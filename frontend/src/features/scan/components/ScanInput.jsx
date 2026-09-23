import Card from "../../../components/common/Card";
import TextArea from "../../../components/common/TextArea";
import Button from "../../../components/common/Button";
import styles from "./ScanInput.module.css";

// Main input area: paste content + trigger a scan.
function ScanInput({ value = "", onChange, onScan, loading = false, disabled = false }) {
  const canScan = value.trim().length > 0 && !loading && !disabled;

  return (
    <Card title="Scan Input">
      <div className={styles.wrapper}>
        <TextArea
          id="scan-input"
          label="Content to scan"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste text, email, source code, or log output here..."
          rows={10}
          disabled={disabled || loading}
        />

        <div className={styles.actions}>
          <span className={styles.hint}>
            {value.trim().length > 0
              ? `${value.length} characters`
              : "Waiting for input..."}
          </span>
          <Button
            variant="primary"
            size="lg"
            onClick={onScan}
            disabled={!canScan}
            loading={loading}
          >
            {loading ? "Scanning..." : "Scan"}
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default ScanInput;
