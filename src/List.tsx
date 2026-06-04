import React, { useEffect, useState } from "react";
import { resolveWebsiteHref } from "./exhibitorUrls";
import { loadMapdata } from "./loadMapdata";
import {
  exhibitorMatchesMapBooth,
  parseFavoriteEntry,
  standLabelMatches,
} from "./standMatching";
import "./normalize.css";
import "./skeleton.css";
import "./index.css";

interface Stand {
  pk?: number;
  label: string;
  points: [number, number][];
  expo_map?: number;
}

interface Exhibitor {
  stand: string;
  title: string;
  description: string;
  website?: string;
  expo_map?: number;
}

function findStand(stands: Stand[], label: string): Stand | undefined {
  return stands.find((s) => standLabelMatches(s.label, label));
}

function findExhibitors(
  exhibitors: Exhibitor[],
  label: string,
  hallPk?: number,
): Exhibitor[] {
  return exhibitors.filter((e) => {
    if (!exhibitorMatchesMapBooth(label, e.stand)) return false;
    if (hallPk == null || e.expo_map == null) return true;
    return Number(e.expo_map) === hallPk;
  });
}

const List: React.FC = () => {
  const [stands, setStands] = useState<Stand[]>([]);
  const [exhibitors, setExhibitors] = useState<Exhibitor[]>([]);
  const [favoriteLists, setFavoriteLists] = useState<
    { key: string; booths: string[] }[]
  >([]);
  const [visited, setVisited] = useState<Record<string, boolean>>({});
  const [mapdataError, setMapdataError] = useState<string | null>(null);

  useEffect(() => {
    setMapdataError(null);
    loadMapdata<{ stands: Stand[]; exhibitors: Exhibitor[] }>()
      .then((data) => {
        setStands(data.stands);
        setExhibitors(data.exhibitors);
        const keys = Object.keys(localStorage)
          .filter((k) => k.startsWith("favorites:"))
          .map((k) => k.replace("favorites:", ""))
          .sort((a, b) => a.localeCompare(b));
        const lists = keys.map((key) => {
          const booths: string[] = JSON.parse(
            localStorage.getItem(`favorites:${key}`) || "[]",
          );
          return { key, booths };
        });
        setFavoriteLists(lists);
        const visitedRaw = localStorage.getItem("visitedBooths") || "{}";
        setVisited(JSON.parse(visitedRaw));
      })
      .catch((err: unknown) => {
        const msg =
          err instanceof Error ? err.message : "Unknown error loading map data.";
        console.error(err);
        setMapdataError(msg);
      });
  }, []);

  const handleVisitedToggle = (label: string) => {
    setVisited((prev) => {
      const updated = { ...prev, [label]: !prev[label] };
      localStorage.setItem("visitedBooths", JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <div className="list-container">
      {mapdataError && (
        <div className="mapdata-load-error" role="alert">
          <strong>Map data failed to load.</strong>
          <p>{mapdataError}</p>
        </div>
      )}
      <h2>Your Lists</h2>
      {favoriteLists.length === 0 && <p>No lists found in storage.</p>}
      {favoriteLists.map((list) => (
        <div key={list.key} style={{ marginBottom: 32 }}>
          <h3 style={{ marginBottom: 8 }}>{list.key}</h3>
          <ul>
            {list.booths.length === 0 && <li>No booths in this list.</li>}
            {list.booths
              .slice()
              .sort((a, b) =>
                a.localeCompare(b, undefined, {
                  numeric: true,
                  sensitivity: "base",
                }),
              )
              .map((entry) => {
                const parsed = parseFavoriteEntry(entry, stands);
                const boothLabel = parsed.label;
                const stand =
                  parsed.standPk != null
                    ? stands.find(
                        (s) =>
                          s.pk === parsed.standPk &&
                          (parsed.hallPk == null ||
                            Number(s.expo_map) === parsed.hallPk),
                      )
                    : findStand(stands, boothLabel);
                const rows = findExhibitors(
                  exhibitors,
                  stand?.label ?? boothLabel,
                  parsed.hallPk,
                );
                const standOnMap = !!stand;
                const title = rows.map((e) => e.title).join(" / ");
                const websiteHref = rows
                  .map((e) => resolveWebsiteHref(e.website))
                  .find(Boolean);
                return (
                  <li
                    key={entry}
                    style={{
                      marginBottom: 16,
                      borderBottom: "1px solid #eee",
                      paddingBottom: 8,
                    }}
                  >
                    <label
                      style={{
                        display: "flex",
                        alignItems: "flex-start",
                        gap: 12,
                      }}
                    >
                      <input
                        type="checkbox"
                        checked={!!visited[entry]}
                        onChange={() => handleVisitedToggle(entry)}
                        style={{ marginTop: 4 }}
                      />
                      <div style={{ flex: 1 }}>
                        <div>
                          <strong>
                            {stand?.label || boothLabel} {title}
                          </strong>
                        </div>
                        {!standOnMap && (
                          <div
                            style={{
                              fontSize: "0.9em",
                              color: "#a63",
                              margin: "4px 0",
                            }}
                          >
                            Not on this year&apos;s map — booth may have moved
                            or been removed.
                          </div>
                        )}
                        {standOnMap && rows.length === 0 && (
                          <div
                            style={{
                              fontSize: "0.9em",
                              color: "#666",
                              margin: "4px 0",
                            }}
                          >
                            No exhibitor listing for this booth in current
                            data.
                          </div>
                        )}
                        {websiteHref && (
                          <div style={{ fontSize: "0.9em", margin: "2px 0" }}>
                            <a
                              href={websiteHref}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              Website
                            </a>
                          </div>
                        )}
                      </div>
                    </label>
                  </li>
                );
              })}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default List;
