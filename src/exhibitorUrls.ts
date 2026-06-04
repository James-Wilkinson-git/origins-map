function trim(s: string | undefined | null): string {
  return (s ?? "").trim();
}

export function resolveWebsiteHref(website?: string | null): string | null {
  const w = trim(website);
  if (!w) return null;
  if (/^https?:\/\//i.test(w)) return w;
  if (w.startsWith("//")) return `https:${w}`;
  return `https://${w}`;
}
