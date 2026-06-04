import fs from "node:fs";
import path from "node:path";

const root = path.join(import.meta.dirname, "..", "dist");
const required = [
  "index.html",
  "mapdata.json",
  "maps/exhibitors.png",
  "maps/gaming-hall.png",
];

for (const rel of required) {
  const file = path.join(root, rel);
  if (!fs.existsSync(file)) {
    console.error(`Missing ${file} — run build-mapdata, ensure public/ assets exist, then npm run build.`);
    process.exit(1);
  }
}

console.log("dist/ OK:", required.join(", "));
