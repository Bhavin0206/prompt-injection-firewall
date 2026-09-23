import Badge from "../../../components/common/Badge";
import { VERDICT } from "../../../utils/constants";
import styles from "./VerdictCard.module.css";

// Result card shown after a scan.
// result = { verdict: "safe" | "blocked", attackType?, reason?, confidence? }
//   - green SAFE   -> nothing dangerous found
//   - red BLOCKED  -> threat detected (attack type + reason + confidence)
function VerdictCard({ result }) {
  if (!result) {
    return (
      <section className={`${styles.card} ${styles.empty}`}>
        <p className={styles.emptyText}>
          No scan results yet — paste content above and click <strong>Scan</strong>.
        </p>
      </section>
    );
  }

  const { verdict, attackType, reason, confidence } = result;
  const isBlocked = verdict === VERDICT.BLOCKED;
  const confidencePct = Math.max(0, Math.min(100, Number(confidence) || 0));

  const tone = isBlocked ? "danger" : "success";
  const statusText = isBlocked ? "BLOCKED" : "SAFE";
  const statusIcon = isBlocked ? "✗" : "✓";

  return (
    <section
      className={`${styles.card} ${styles[tone]}`}
      aria-live="polite"
      data-testid="verdict-card"
    >
      <header className={styles.header}>
        <span className={`${styles.status} ${styles[tone]}`}>
          <span className={styles.icon} aria-hidden="true">
            {statusIcon}
          </span>
          {statusText}
        </span>

        {isBlocked ? (
          attackType ? <Badge variant="danger">{attackType}</Badge> : null
        ) : (
          <Badge variant="success">No threats detected</Badge>
        )}
      </header>

      {reason && <p className={styles.reason}>{reason}</p>}

      <div className={styles.confidence}>
        <div className={styles.confidenceLabel}>
          <span>Confidence</span>
          <span className={styles.confidenceValue}>{confidencePct}%</span>
        </div>
        <div
          className={styles.track}
          role="progressbar"
          aria-valuenow={confidencePct}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className={`${styles.fill} ${styles[tone]}`}
            style={{ width: `${confidencePct}%` }}
          />
        </div>
      </div>
    </section>
  );
}

export default VerdictCard;