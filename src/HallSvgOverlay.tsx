import React, { useMemo } from "react";
import { SVGOverlay } from "react-leaflet";
import type { LatLngBounds } from "leaflet";
import { isFavoritedBooth, standLabelMatches } from "./standMatching";

export function parseViewBoxString(
  raw: string | undefined,
): { vx: number; vy: number; vw: number; vh: number } | null {
  if (!raw?.trim()) return null;
  const p = raw.trim().split(/\s+/).map(Number);
  if (p.length < 4 || p.some((n) => !Number.isFinite(n))) return null;
  return { vx: p[0]!, vy: p[1]!, vw: p[2]!, vh: p[3]! };
}

export function ringToSvgPoints(ring: [number, number][]): string {
  return ring.map(([x, y]) => `${x},${y}`).join(" ");
}

const BOOTH_OUTLINE_STROKE = "#141414";
const BOOTH_OUTLINE_WIDTH = 1.25;
/** Favorites and search focus share yellow so booth numbers stay readable on the PDF. */
const YELLOW_HIGHLIGHT_FILL = "#ffeb3b";
const YELLOW_HIGHLIGHT_STROKE = "#fbc02d";
const YELLOW_HIGHLIGHT_STROKE_WIDTH = 1.5;
const FAVORITE_FILL_OPACITY = 0.38;
const SEARCH_FOCUS_FILL_OPACITY = 0.48;
const SEARCH_MATCH_FILL = "#e3f2fd";
const SEARCH_MATCH_FILL_OPACITY = 0.35;
const SEARCH_MATCH_STROKE = "#1565c0";
const SEARCH_MATCH_STROKE_WIDTH = 1.25;

export function standSvgStyle(
  standPk: number,
  label: string,
  hallPk: number,
  labelCountInHall: number,
  favorites: string[],
  searchActive: boolean,
  highlightPks: Set<number>,
  searchFocusStand: string | null,
): React.SVGProps<SVGPolygonElement> {
  const base = {
    style: {
      pointerEvents: "none" as const,
      strokeLinejoin: "round" as const,
    },
  };

  const inHighlight = highlightPks.has(standPk);
  const isFocus =
    searchFocusStand != null &&
    inHighlight &&
    standLabelMatches(label, searchFocusStand);
  const isMatch = searchActive && inHighlight && !isFocus;
  const isFavorite = isFavoritedBooth(
    hallPk,
    standPk,
    label,
    favorites,
    labelCountInHall,
  );

  if (isFocus) {
    return {
      ...base,
      fill: YELLOW_HIGHLIGHT_FILL,
      fillOpacity: SEARCH_FOCUS_FILL_OPACITY,
      stroke: YELLOW_HIGHLIGHT_STROKE,
      strokeWidth: YELLOW_HIGHLIGHT_STROKE_WIDTH,
    };
  }

  if (searchActive) {
    if (isMatch) {
      return {
        ...base,
        fill: SEARCH_MATCH_FILL,
        fillOpacity: SEARCH_MATCH_FILL_OPACITY,
        stroke: SEARCH_MATCH_STROKE,
        strokeWidth: SEARCH_MATCH_STROKE_WIDTH,
      };
    }
    if (isFavorite) {
      return {
        ...base,
        fill: YELLOW_HIGHLIGHT_FILL,
        fillOpacity: FAVORITE_FILL_OPACITY,
        stroke: YELLOW_HIGHLIGHT_STROKE,
        strokeWidth: YELLOW_HIGHLIGHT_STROKE_WIDTH,
      };
    }
    return {
      ...base,
      fill: "none",
      stroke: BOOTH_OUTLINE_STROKE,
      strokeWidth: BOOTH_OUTLINE_WIDTH,
      opacity: 0.35,
    };
  }

  if (isFavorite) {
    return {
      ...base,
      fill: YELLOW_HIGHLIGHT_FILL,
      fillOpacity: FAVORITE_FILL_OPACITY,
      stroke: YELLOW_HIGHLIGHT_STROKE,
      strokeWidth: YELLOW_HIGHLIGHT_STROKE_WIDTH,
    };
  }

  return {
    ...base,
    fill: "none",
    stroke: BOOTH_OUTLINE_STROKE,
    strokeWidth: BOOTH_OUTLINE_WIDTH,
    opacity: 1,
  };
}

export function HallSvgOverlay({
  bounds,
  viewBoxStr,
  vb,
  imageUrl,
  children,
}: {
  bounds: LatLngBounds;
  viewBoxStr: string;
  vb: { vx: number; vy: number; vw: number; vh: number };
  imageUrl: string;
  children: React.ReactNode;
}) {
  const attrs = useMemo(
    () => ({
      viewBox: viewBoxStr,
      preserveAspectRatio: "none",
      class: "origins-expo-svg",
    }),
    [viewBoxStr],
  );

  return (
    <SVGOverlay bounds={bounds} interactive={false} attributes={attrs}>
      <image
        href={imageUrl}
        x={vb.vx}
        y={vb.vy}
        width={vb.vw}
        height={vb.vh}
        preserveAspectRatio="none"
        style={{ pointerEvents: "none" }}
      />
      {children}
    </SVGOverlay>
  );
}
