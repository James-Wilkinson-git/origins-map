import {
  compressToEncodedURIComponent,
  decompressFromEncodedURIComponent,
} from "lz-string";

export function parseHashParams(): URLSearchParams {
  const raw = window.location.hash.startsWith("#")
    ? window.location.hash.substring(1)
    : window.location.hash;
  if (!raw) return new URLSearchParams();
  return new URLSearchParams(raw.startsWith("?") ? raw : `?${raw}`);
}

export function decodeFavoritesParam(favEncoded: string | null): string[] {
  if (!favEncoded) return [];
  try {
    const decoded = decompressFromEncodedURIComponent(favEncoded);
    if (!decoded) return [];
    return decoded
      .split(",")
      .map((f) => f.trim())
      .filter(Boolean);
  } catch {
    return [];
  }
}

/** Read list name + booths from the URL hash (share links). */
export function favoritesFromHash(): {
  listKey: string | null;
  favorites: string[];
  hasFavsParam: boolean;
} {
  const params = parseHashParams();
  const listKey = params.get("list");
  if (!listKey) {
    return { listKey: null, favorites: [], hasFavsParam: false };
  }
  const favEncoded = params.get("favs");
  const hasFavsParam = favEncoded != null && favEncoded !== "";
  const favorites = hasFavsParam ? decodeFavoritesParam(favEncoded) : [];
  return { listKey, favorites, hasFavsParam };
}

export function persistList(listKey: string, favorites: string[]): void {
  localStorage.setItem(`favorites:${listKey}`, JSON.stringify(favorites));
}

export function writeListHash(listKey: string, favorites: string[]): void {
  const compressed = compressToEncodedURIComponent(favorites.join(","));
  const next = `#list=${encodeURIComponent(listKey)}&favs=${compressed}`;
  if (window.location.hash === next) return;
  window.history.replaceState(
    null,
    "",
    `${window.location.pathname}${window.location.search}${next}`,
  );
}

/** Hydrate React state from hash on first paint (before effects run). */
export function initialListState(): {
  listKey: string | null;
  favorites: string[];
} {
  const { listKey, favorites, hasFavsParam } = favoritesFromHash();
  if (!listKey) {
    return { listKey: null, favorites: [] };
  }
  if (hasFavsParam) {
    persistList(listKey, favorites);
    return { listKey, favorites };
  }
  try {
    const stored = JSON.parse(
      localStorage.getItem(`favorites:${listKey}`) || "[]",
    );
    const favs = Array.isArray(stored) ? stored : [];
    persistList(listKey, favs);
    return { listKey, favorites: favs };
  } catch {
    persistList(listKey, []);
    return { listKey, favorites: [] };
  }
}
