import Spinner from "../../../components/common/Spinner";
import styles from "./AgentStatus.module.css";

// Shown while the agent is running (fetching + scanning can take a few seconds).
function AgentStatus({ loading }) {
  if (!loading) return null;

  return (
    <div className={styles.status} role="status" aria-live="polite">
      <Spinner size="sm" />
      <div className={styles.text}>
        <span className={styles.title}>Agent is running…</span>
        <span className={styles.hint}>
          fetching content and scanning every item. This can take a few seconds.
        </span>
      </div>
    </div>
  );
}

export default AgentStatus;
