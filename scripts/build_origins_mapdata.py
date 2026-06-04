#!/usr/bin/env python3
"""
Extract booth polygons from Origins PDF floor plans + merge exhibitor TSV → public/mapdata.json.

Run from repo root: npm run build-mapdata
"""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path
from typing import Any

import fitz

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PUBLIC = ROOT / "public"
MAPS_DIR = PUBLIC / "maps"
OUT_MAPDATA = PUBLIC / "mapdata.json"
OUT_AUDIT = ROOT / "scripts" / "booth-audit.json"
OVERRIDES_PATH = DATA / "booth-overrides.json"

PDF_EXHIBITORS = Path(r"C:/Users/james/Desktop/Origins+Exhibitors+Map+Full.pdf")
PDF_GAMING = Path(r"C:/Users/james/Desktop/Origins+Gaming+Hall+Map.pdf")

GAMING_LEGEND_MIN_X = 450.0
GAMING_MAP_MAX_X = 450.0

# Raster scale (PDF points → pixels). 5× ≈ 4060px wide for exhibit hall.
RENDER_SCALE = 5.0
# Padding below last booth rectangle (entrances/labels sit just under the grid).
EXHIBITORS_MAP_PADDING = 18.0

MIN_RECT_AREA = 50.0
MAX_RECT_AREA = 80_000.0
LABEL_MAX_DIST = 45.0

MAP_EXHIBITORS_PK = 1
MAP_GAMING_PK = 2

BOOTH_NUM_RE = re.compile(r"^\d{3,5}$")


def rect_area(r: fitz.Rect) -> float:
    return abs(r.width * r.height)


def rect_center(r: fitz.Rect) -> tuple[float, float]:
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


def dist_point_rect(px: float, py: float, r: fitz.Rect) -> float:
    dx = max(r.x0 - px, 0.0, px - r.x1)
    dy = max(r.y0 - py, 0.0, py - r.y1)
    return math.hypot(dx, dy)


def rect_to_points(r: fitz.Rect) -> list[list[float]]:
    return [
        [r.x0, r.y0],
        [r.x1, r.y0],
        [r.x1, r.y1],
        [r.x0, r.y1],
    ]


def split_label(label: str) -> list[str]:
    parts = re.split(r"[/,]", label)
    out = [p.strip() for p in parts if p.strip()]
    return out or [label.strip()]


def normalize_website(url: str) -> str:
    u = (url or "").strip()
    if not u:
        return ""
    if re.match(r"^https?://", u, re.I):
        return u
    if u.startswith("//"):
        return f"https:{u}"
    return f"https://{u}"


def load_tsv(path: Path, hall_pk: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for i, row in enumerate(reader):
            name = (row.get("Exhibiting As Name") or row.get("name") or "").strip()
            booth_raw = (row.get("Booth Number") or row.get("Supported Play Space Hall C Room Number") or row.get("booth") or "").strip()
            website = normalize_website(row.get("Website") or row.get("website") or "")
            if not booth_raw:
                continue
            for booth in re.split(r"[,/]", booth_raw):
                booth = booth.strip()
                if not booth:
                    continue
                rows.append(
                    {
                        "pk": len(rows) + 1,
                        "title": name,
                        "stand": booth,
                        "website": website,
                        "description": "",
                        "url": "",
                        "hall_pk": hall_pk,
                    }
                )
    return rows


def load_overrides() -> dict[str, Any]:
    if not OVERRIDES_PATH.is_file():
        return {"stands": []}
    return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))


def extract_booth_rects(page: fitz.Page, max_y: float | None = None) -> list[fitz.Rect]:
    rects: list[fitz.Rect] = []
    for d in page.get_drawings():
        for item in d.get("items", []):
            if item[0] != "re":
                continue
            r = fitz.Rect(item[1])
            a = rect_area(r)
            if a < MIN_RECT_AREA or a > MAX_RECT_AREA:
                continue
            if max_y is not None:
                cy = rect_center(r)[1]
                if cy > max_y:
                    continue
            rects.append(r)
    return rects


def extract_booth_labels(
    page: fitz.Page,
    *,
    max_y: float | None = None,
    max_x: float | None = None,
    min_x: float | None = None,
) -> list[tuple[str, fitz.Rect]]:
    labels: list[tuple[str, fitz.Rect]] = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            for sp in line["spans"]:
                t = sp["text"].strip()
                if not BOOTH_NUM_RE.fullmatch(t):
                    continue
                bb = fitz.Rect(sp["bbox"])
                if max_y is not None and bb.y0 > max_y:
                    continue
                if max_x is not None and bb.x0 > max_x:
                    continue
                if min_x is not None and bb.x1 < min_x:
                    continue
                labels.append((t, bb))
    return labels


def assign_labels_to_rects(
    rects: list[fitz.Rect],
    labels: list[tuple[str, fitz.Rect]],
) -> dict[int, list[str]]:
    """Map rect index -> list of booth label strings."""
    assigned: dict[int, list[str]] = {i: [] for i in range(len(rects))}
    for text, bb in labels:
        cx, cy = rect_center(bb)
        best_i: int | None = None
        best_d = 1e9
        for i, r in enumerate(rects):
            d = dist_point_rect(cx, cy, r)
            if d < best_d:
                best_d = d
                best_i = i
        if best_i is not None and best_d <= LABEL_MAX_DIST:
            if text not in assigned[best_i]:
                assigned[best_i].append(text)
    return assigned


def assign_legend_column_to_rects(
    rects: list[fitz.Rect],
    labels: list[tuple[str, fitz.Rect]],
    legend_min_x: float,
) -> dict[int, list[str]]:
    """Gaming hall: right-column booth list — match by similar Y to nearest rect left of legend."""
    assigned: dict[int, list[str]] = {i: [] for i in range(len(rects))}
    for text, bb in labels:
        if bb.x0 < legend_min_x:
            continue
        cy = rect_center(bb)[1]
        best_i: int | None = None
        best_dy = 1e9
        for i, r in enumerate(rects):
            if r.x1 > legend_min_x - 20:
                continue
            dy = abs(rect_center(r)[1] - cy)
            if dy < best_dy:
                best_dy = dy
                best_i = i
        if best_i is not None and best_dy <= 35:
            if text not in assigned[best_i]:
                assigned[best_i].append(text)
    return assigned


def build_stands_from_pdf(
    page: fitz.Page,
    expo_map: int,
    *,
    max_y: float | None = None,
    label_max_x: float | None = None,
    legend_min_x: float | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    rects = extract_booth_rects(page, max_y=max_y)
    labels = extract_booth_labels(page, max_y=max_y, max_x=label_max_x)
    by_rect = assign_labels_to_rects(rects, labels)
    map_labels_by_rect = {i: list(v) for i, v in by_rect.items()}
    if legend_min_x is not None:
        all_labels = extract_booth_labels(page, max_y=max_y)
        legend_map = assign_legend_column_to_rects(rects, all_labels, legend_min_x)
        for i, extra in legend_map.items():
            # Legend column matches by row Y only — skip if the booth already has an on-map label.
            if map_labels_by_rect.get(i):
                continue
            for t in extra:
                if t not in by_rect[i]:
                    by_rect[i].append(t)

    stands: list[dict[str, Any]] = []
    stand_ids: list[str] = []
    pk = 0

    for i, r in enumerate(rects):
        label_texts = by_rect.get(i) or []
        if not label_texts:
            continue
        points = rect_to_points(r)
        for raw in label_texts:
            for alias in split_label(raw):
                pk += 1
                stands.append(
                    {
                        "pk": pk,
                        "label": alias,
                        "points": points,
                        "expo_map": expo_map,
                    }
                )
                if alias not in stand_ids:
                    stand_ids.append(alias)

    return stands, stand_ids


def exhibitors_map_max_y(page: fitz.Page) -> float:
    """Crop above the three-column exhibitor directory (starts ~y=670 on the PDF)."""
    max_rect_bottom = 0.0
    for d in page.get_drawings():
        for item in d.get("items", []):
            if item[0] != "re":
                continue
            r = fitz.Rect(item[1])
            a = rect_area(r)
            if MIN_RECT_AREA < a < MAX_RECT_AREA:
                max_rect_bottom = max(max_rect_bottom, r.y1)
    if max_rect_bottom <= 0:
        return 1005.0
    return max_rect_bottom + EXHIBITORS_MAP_PADDING


def render_map_png(
    page: fitz.Page,
    out_path: Path,
    clip: fitz.Rect | None,
    scale: float = RENDER_SCALE,
) -> None:
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    mat = fitz.Matrix(scale, scale)
    if clip is not None:
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    else:
        pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(str(out_path))


def audit(
    hall_name: str,
    tsv_booths: set[str],
    pdf_labels: set[str],
    stand_ids: list[str],
) -> dict[str, Any]:
    geom = set(stand_ids)
    missing_geom = sorted(tsv_booths - geom)
    extra_geom = sorted(geom - tsv_booths)
    return {
        "hall": hall_name,
        "tsv_booth_count": len(tsv_booths),
        "geometry_booth_count": len(geom),
        "pdf_label_count": len(pdf_labels),
        "tsv_without_geometry": missing_geom,
        "geometry_without_tsv": extra_geom[:50],
        "geometry_without_tsv_total": len(extra_geom),
        "match_rate": round(
            (len(tsv_booths & geom) / len(tsv_booths) * 100) if tsv_booths else 0,
            1,
        ),
    }


def main() -> None:
    exhibitors_tsv = load_tsv(DATA / "exhibitors-hall.tsv", MAP_EXHIBITORS_PK)
    gaming_tsv = load_tsv(DATA / "gaming-hall.tsv", MAP_GAMING_PK)

    doc_ex = fitz.open(PDF_EXHIBITORS)
    page_ex = doc_ex[0]
    ex_w, _ex_h = page_ex.rect.width, page_ex.rect.height
    ex_map_max_y = exhibitors_map_max_y(page_ex)
    ex_clip = fitz.Rect(0, 0, ex_w, ex_map_max_y)

    ex_stands, ex_stand_ids = build_stands_from_pdf(
        page_ex,
        MAP_EXHIBITORS_PK,
        max_y=ex_map_max_y,
    )
    ex_labels = {
        t for t, _ in extract_booth_labels(page_ex, max_y=ex_map_max_y)
    }

    render_map_png(page_ex, MAPS_DIR / "exhibitors.png", ex_clip)
    print(f"  Exhibit Hall crop: 0 0 {ex_w:.1f} {ex_map_max_y:.1f} @ {RENDER_SCALE}x")
    doc_ex.close()

    doc_gh = fitz.open(PDF_GAMING)
    page_gh = doc_gh[0]
    gh_w, gh_h = page_gh.rect.width, page_gh.rect.height

    gh_stands, gh_stand_ids = build_stands_from_pdf(
        page_gh,
        MAP_GAMING_PK,
        label_max_x=GAMING_LEGEND_MIN_X,
        legend_min_x=GAMING_LEGEND_MIN_X,
    )
    gh_labels = {
        t
        for t, _ in extract_booth_labels(page_gh, max_x=GAMING_LEGEND_MIN_X)
    }

    gh_clip = fitz.Rect(0, 0, GAMING_MAP_MAX_X, gh_h)
    render_map_png(page_gh, MAPS_DIR / "gaming-hall.png", gh_clip)
    print(f"  Gaming Hall crop: 0 0 {GAMING_MAP_MAX_X:.1f} {gh_h:.1f} @ {RENDER_SCALE}x")
    doc_gh.close()

    overrides = load_overrides()
    for row in overrides.get("stands", []):
        pk = row.get("expo_map")
        if pk == MAP_EXHIBITORS_PK:
            ex_stands.append(row)
            if row["label"] not in ex_stand_ids:
                ex_stand_ids.append(row["label"])
        elif pk == MAP_GAMING_PK:
            gh_stands.append(row)
            if row["label"] not in gh_stand_ids:
                gh_stand_ids.append(row["label"])

    exhibitors = [
        {
            "pk": e["pk"],
            "title": e["title"],
            "stand": e["stand"],
            "website": e["website"],
            "description": e["description"],
            "url": e["url"],
            "expo_map": e["hall_pk"],
        }
        for e in exhibitors_tsv + gaming_tsv
    ]

    maps = [
        {
            "pk": MAP_EXHIBITORS_PK,
            "title": "Exhibit Hall",
            "view_box": f"0 0 {ex_w} {ex_map_max_y}",
            "bounds": f"0 0 {ex_w} {ex_map_max_y}",
            "flattened_image": "/maps/exhibitors.png",
            "image": "/maps/exhibitors.png",
            "stands": ex_stand_ids,
        },
        {
            "pk": MAP_GAMING_PK,
            "title": "Gaming Hall C",
            "view_box": f"0 0 {GAMING_MAP_MAX_X} {gh_h}",
            "bounds": f"0 0 {GAMING_MAP_MAX_X} {gh_h}",
            "flattened_image": "/maps/gaming-hall.png",
            "image": "/maps/gaming-hall.png",
            "stands": gh_stand_ids,
        },
    ]

    all_stands = ex_stands + gh_stands
    mapdata = {
        "maps": maps,
        "stands": all_stands,
        "exhibitors": exhibitors,
        "categories": [],
    }

    PUBLIC.mkdir(parents=True, exist_ok=True)
    OUT_MAPDATA.write_text(json.dumps(mapdata, indent=2), encoding="utf-8")

    audit_report = {
        "exhibitors": audit(
            "Exhibit Hall",
            {e["stand"] for e in exhibitors_tsv},
            ex_labels,
            ex_stand_ids,
        ),
        "gaming": audit(
            "Gaming Hall C",
            {e["stand"] for e in gaming_tsv},
            gh_labels,
            gh_stand_ids,
        ),
    }
    OUT_AUDIT.write_text(json.dumps(audit_report, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_MAPDATA} ({len(all_stands)} stands, {len(exhibitors)} exhibitor rows)")
    print(f"Wrote {OUT_AUDIT}")
    for key, a in audit_report.items():
        print(
            f"  {a['hall']}: {a['match_rate']}% TSV matched "
            f"({a['tsv_booth_count']} TSV, {a['geometry_booth_count']} geom)"
        )


if __name__ == "__main__":
    main()
