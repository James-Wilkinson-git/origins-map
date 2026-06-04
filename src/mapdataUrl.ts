export function mapdataUrl(): string {
  const base = import.meta.env.BASE_URL;
  return `${base.endsWith("/") ? base : `${base}/`}mapdata.json`;
}

export function publicAssetUrl(path: string): string {
  const p = path.trim();
  if (!p || /^https?:\/\//i.test(p) || p.startsWith("//")) return p;
  const base = import.meta.env.BASE_URL;
  const withSlash = base.endsWith("/") ? base : `${base}/`;
  const pathPart = p.startsWith("/") ? p.slice(1) : p;
  return `${withSlash}${pathPart}`;
}
