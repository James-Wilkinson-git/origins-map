# Origins 2026 Interactive Map

Interactive floor plans for Origins Game Fair exhibit hall and Gaming Hall C, built with React, Vite, and Leaflet. Same UX as the UKGE map: sidebar search, adventure-plan lists, favorites, share links, list view, and print/PNG export.

## Setup

```bash
npm install
npm run build-mapdata   # requires Python 3 + PyMuPDF; reads PDFs from Desktop
npm run dev
```

PDF sources (default paths in `scripts/build_origins_mapdata.py`):

- `Origins+Exhibitors+Map+Full.pdf`
- `Origins+Gaming+Hall+Map.pdf`

Exhibitor lists live in `data/exhibitors-hall.tsv` and `data/gaming-hall.tsv`.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Vite dev server |
| `npm run build` | Production build to `dist/` |
| `npm run build-mapdata` | Extract booth polygons from PDFs → `public/mapdata.json` |

## Data pipeline

1. PyMuPDF extracts vector booth rectangles and booth-number labels from each PDF.
2. Labels are matched to rectangles (map cells + gaming-hall legend column).
3. TSV exhibitor rows are merged into `mapdata.json`.
4. Floor PNGs are cropped only: exhibit hall below the booth grid (~y 673+ directory), gaming legend column (`x ≥ 450`). Rendered at **5×** resolution (~4000px wide for exhibit hall).
5. `scripts/booth-audit.json` reports TSV ↔ geometry coverage.

Optional manual fixes: `data/booth-overrides.json`.

## Deploy to Render

This app is a **static site** (Vite → `dist/`). Map PNGs and `mapdata.json` must live in `public/` before deploy — Render does not run the Python PDF pipeline.

1. Regenerate assets locally when data changes:
   ```bash
   npm run build-mapdata
   npm run build
   ```
   Confirm `dist/mapdata.json` and `dist/maps/*.png` exist.
2. Commit `public/mapdata.json`, `public/maps/`, and `package-lock.json` to git.
3. On [Render](https://render.com):
   - **Blueprint:** connect the repo; Render reads `render.yaml` (build `npm ci && npm run build`, publish `dist`, SPA rewrite `/*` → `/index.html`).
   - **Manual static site:** Build command `npm ci && npm run build`, Publish directory `dist`, and add redirect/rewrite **Rewrite** `/*` → `/index.html`.
4. After deploy, smoke-test `/`, `/list`, and a hard refresh on `/list` (should not 404).

`npm run preview` locally mimics production static hosting (without the SPA rewrite; use Render or add a local rewrite if testing deep links).
