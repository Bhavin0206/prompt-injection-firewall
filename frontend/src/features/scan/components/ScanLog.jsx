import Card from "../../../components/common/Card";
import Badge from "../../../components/common/Badge";
import { VERDICT } from "../../../utils/constants";
import styles from "./ScanLog.module.css";

// Format a date for display: "14:32:05" for today, "Sep 24 · 14:32" otherwise.
function formatTime(at) {
  const date = at instanceof Date ? at : new Date(at);
  if (Number.isNaN(date.getTime())) return "";

  if (date.toDateString() === new Date().toDateString()) {
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }
  return `${date.toLocaleDateString([], { month: "short", day: "numeric" })} · ${date.toLocaleTimeString(
    [],
    { hour: "2-digit", minute: "2-digit" }
  )}`;
}

// Sidebar log of past scans.
// entries = [{ id, at, verdict, attackType?, reason?, confidence? }]
function ScanLog({ entries = [], onSelect, emptyText = "No scans yet — run one above." }) {
  const clickable = typeof onSelect === "function";

  return (
    <Card title="Scan Log">
      <ul className={styles.list}>
        {entries.length === 0 ? (
          <li>
            <p className={styles.empty}>{emptyText}</p>
          </li>
        ) : (
          entries.map((entry) => {
            const isBlocked = entry.verdict === VERDICT.BLOCKED;

            return (
              <li key={entry.id ?? entry.at}>
                <button
                  type="button"
                  className={`${styles.row} ${clickable ? styles.clickable : ""}`}
                  onClick={() => clickable && onSelect(entry)}
                  disabled={!clickable}
                  title={entry.reason}
                >
                  <span className={styles.time}>{formatTime(entry.at)}</span>
                  <Badge variant={isBlocked ? "danger" : "success"}>
                    {isBlocked ? "BLOCKED" : "SAFE"}
                  </Badge>
                  <span className={styles.attackType}>
                    {isBlocked ? entry.attackType ?? "Threat detected" : "No threats"}
                  </span>
                </button>
              </li>
            );
          })
        )}
      </ul>
    </Card>
  );
}

export default ScanLog;