import Spinner from "../../../components/common/Spinner";
import styles from "./ScanStatus.module.css";

// Inline feedback between the input and the verdict card:
//   - loading -> spinner + "Scanning content…"
//   - error   -> friendly alert with a retry hint
// Renders nothing when idle.
function ScanStatus({ loading = false, error = "" }) {
  if (loading) {
    return (
      <div className={styles.loading} role="status" aria-live="polite">
        <Spinner size="lg" label="Scanning content" />
        <div className={styles.loadingText}>
          <span className={styles.loadingTitle}>Scanning content…</span>
          <span className={styles.loadingHint}>
            Checking for prompt injections and malicious instructions.
          </span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorCard} role="alert">
        <span className={styles.errorIcon} aria-hidden="true">
          ⚠
        </span>
        <div className={styles.errorBody}>
          <p className={styles.errorTitle}>Scan failed</p>
          <p className={styles.errorMessage}>{error}</p>
          <p className={styles.errorHint}>Check your content and try again.</p>
        </div>
      </div>
    );
  }

  return null;
}

export default ScanStatus;