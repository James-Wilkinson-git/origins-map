import { LatLng } from "leaflet";

/** SVG viewBox coords → Leaflet CRS.Simple (lat = -y, lng = x). */
export function svgPointToLatLngTuple([x, y]: [number, number]): [number, number] {
  return [-y, x];
}

export function svgPointToLatLng([x, y]: [number, number]): LatLng {
  return new LatLng(-y, x);
}
