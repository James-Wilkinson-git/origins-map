export function splitStandLabel(label: string): string[] {
  return label
    .split(/[/,]/)
    .map((p) => p.trim())
    .filter(Boolean);
}

export function standLabelMatches(
  mapLabel: string,
  exhibitorStand: string,
): boolean {
  const a = mapLabel.trim().toLowerCase();
  const b = exhibitorStand.trim().toLowerCase();
  if (a === b) return true;
  return splitStandLabel(mapLabel).some((p) => p.toLowerCase() === b);
}

/** Exhibitor row applies to this map booth cell (avoids matching the wrong booth when a company has multiple stands). */
export function exhibitorMatchesMapBooth(
  mapLabel: string,
  exhibitorStand: string,
): boolean {
  const mapParts = splitStandLabel(mapLabel).map((p) => p.toLowerCase());
  const exParts = splitStandLabel(exhibitorStand).map((p) => p.toLowerCase());
  return exParts.some((ex) => mapParts.includes(ex));
}

export function mapHasStand(
  stands: string[],
  exhibitorStand: string,
): boolean {
  return stands.some((s) => standLabelMatches(s, exhibitorStand));
}

export function favoriteStorageId(hallPk: number, standPk: number): string {
  return `${hallPk}:${standPk}`;
}

export function isFavorited(
  mapLabel: string,
  favorites: string[],
): boolean {
  return favorites.some((f) => standLabelMatches(mapLabel, f));
}

export function isFavoritedBooth(
  hallPk: number,
  standPk: number,
  mapLabel: string,
  favorites: string[],
  /** How many polygons in this hall use `mapLabel`. */
  labelCountInHall: number,
): boolean {
  const id = favoriteStorageId(hallPk, standPk);
  if (favorites.includes(id)) return true;
  if (labelCountInHall !== 1) return false;
  return favorites.some(
    (f) => !f.includes(":") && standLabelMatches(mapLabel, f),
  );
}

export function parseFavoriteEntry(
  entry: string,
  stands: { pk?: number; label: string; expo_map?: number }[],
): { hallPk?: number; standPk?: number; label: string } {
  const colon = entry.indexOf(":");
  if (colon > 0) {
    const hallPk = Number(entry.slice(0, colon));
    const standPk = Number(entry.slice(colon + 1));
    if (Number.isFinite(hallPk) && Number.isFinite(standPk)) {
      const row = stands.find(
        (s) =>
          s.pk === standPk &&
          (s.expo_map == null || Number(s.expo_map) === hallPk),
      );
      return {
        hallPk,
        standPk,
        label: row?.label ?? entry,
      };
    }
  }
  return { label: entry };
}

export function toggleFavoriteId(
  hallPk: number,
  standPk: number,
  mapLabel: string,
  favorites: string[],
  labelCountInHall: number,
): string[] {
  const id = favoriteStorageId(hallPk, standPk);
  const hasId = favorites.includes(id);
  const hasLegacy =
    labelCountInHall === 1 &&
    favorites.some((f) => !f.includes(":") && standLabelMatches(mapLabel, f));

  if (hasId || hasLegacy) {
    return favorites.filter(
      (f) =>
        f !== id &&
        !(labelCountInHall === 1 && standLabelMatches(mapLabel, f)),
    );
  }
  return [...favorites, id];
}
