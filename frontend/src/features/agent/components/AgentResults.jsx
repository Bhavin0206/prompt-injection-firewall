import { useState } from "react";
import Card from "../../../components/common/Card";
import Badge from "../../../components/common/Badge";
import styles from "./AgentResults.module.css";

// Dashboard for one agent run: big counts + clickable items that reveal the
// firewall's reason.
function AgentResults({ summary, results = [], errors = [] }) {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <Card title="Results">
      <div className={styles.counts}>
        <div className={styles.count}>
          <strong className={styles.countValue}>{summary.fetched}</strong>
          <span className={styles.countLabel}>Fetched</span>
        </div>
        <div className={styles.count}>
          <strong className={`${styles.countValue} ${styles.danger}`}>
            {summary.blocked}
          </strong>
          <span className={styles.countLabel}>Blocked</span>
        </div>
        <div className={styles.count}>
          <strong className={`${styles.countValue} ${styles.success}`}>
            {summary.passed}
          </strong>
          <span className={styles.countLabel}>Passed</span>
        </div>
      </div>

      {results.length > 0 && (
        <p className={styles.listHint}>Click an item to see why it was blocked.</p>
      )}

      <ul className={styles.list}>
        {results.map((item, index) => {
          const isOpen = openIndex === index;
          return (
            <li key={`${item.label}-${index}`}>
              <button
                type="button"
                className={`${styles.row} ${isOpen ? styles.rowOpen : ""}`}
                onClick={() => setOpenIndex(isOpen ? null : index)}
                aria-expanded={isOpen}
              >
                <Badge variant={item.blocked ? "danger" : "success"}>
                  {item.verdict.toUpperCase()}
                </Badge>
                <span className={styles.label} title={item.label}>
                  {item.label}
                </span>
                {item.attackType && (
                  <span className={styles.tag}>{item.attackType}</span>
                )}
                <span
                  className={`${styles.chevron} ${isOpen ? styles.chevronOpen : ""}`}
                  aria-hidden="true"
                >
                  ▾
                </span>
              </button>

              {isOpen && (
                <div className={styles.detail}>
                  <p className={styles.reason}>{item.reason}</p>
                  <p className={styles.meta}>
                    source: <strong>{item.source || "-"}</strong> · confidence:{" "}
                    <strong>{item.confidence}%</strong> · action:{" "}
                    <strong>{item.action || "-"}</strong>
                  </p>
                </div>
              )}
            </li>
          );
        })}
      </ul>

      {errors.length > 0 && (
        <ul className={styles.errors}>
          {errors.map((error, index) => (
            <li key={index}>⚠ {error}</li>
          ))}
        </ul>
      )}
    </Card>
  );
}

export default AgentResults;
