import { LatLng, LatLngBounds } from "leaflet";
import { svgPointToLatLng } from "./mapCoords";
import { standLabelMatches } from "./standMatching";

export interface ExhibitorRow {
  stand: string;
  title: string;
  description: string;
  website?: string;
  expo_map?: number;
}

export interface MapInfoLite {
  pk?: number;
  title: string;
  stands: string[];
}

export interface StandGeometry {
  pk?: number;
  label: string;
  points: [number, number][];
  expo_map?: number;
}

export function normalizeSearchText(s: string): string {
  return s.trim().toLowerCase();
}

export interface StandSearchResult {
  stand: string;
  title: string;
  description: string;
  hallTitle: string;
}

export function searchExhibitorsByStand(
  exhibitors: ExhibitorRow[],
  maps: MapInfoLite[],
  query: string,
): StandSearchResult[] {
  const q = normalizeSearchText(query);
  if (!q) return [];

  const byStand = new Map<string, ExhibitorRow[]>();
  for (const e of exhibitors) {
    const arr = byStand.get(e.stand) ?? [];
    arr.push(e);
    byStand.set(e.stand, arr);
  }

  const results: StandSearchResult[] = [];
  for (const [stand, rows] of byStand) {
    const title = rows.map((r) => r.title).join(" / ");
    const description = rows.map((r) => r.description).join("\n\n");
    const haystack = normalizeSearchText(`${stand} ${title} ${description}`);
    if (!haystack.includes(q)) continue;
    const hallPk = rows[0]?.expo_map;
    const hall =
      hallPk != null
        ? maps.find((m) => Number(m.pk) === Number(hallPk))
        : mapForStand(maps, stand);
    results.push({
      stand,
      title,
      description,
      hallTitle: hall?.title ?? "Unknown hall",
    });
  }

  results.sort((a, b) =>
    a.stand.localeCompare(b.stand, undefined, {
      numeric: true,
      sensitivity: "base",
    }),
  );
  return results;
}

export function mapForStand(
  maps: MapInfoLite[],
  standLabel: string,
): MapInfoLite | undefined {
  return maps.find((m) =>
    m.stands.some((s) => standLabelMatches(s, standLabel)),
  );
}

export function boundsForStandGeometry(
  stands: StandGeometry[],
  standLabel: string,
  standPk?: number,
): LatLngBounds | null {
  let b: LatLngBounds | null = null;
  for (const s of stands) {
    if (standPk != null && s.pk != null && s.pk !== standPk) continue;
    if (!standLabelMatches(s.label, standLabel)) continue;
    for (const xy of s.points) {
      const ll = svgPointToLatLng(xy);
      if (!b) b = new LatLngBounds(ll, ll);
      else b.extend(ll);
    }
  }
  return b;
}
