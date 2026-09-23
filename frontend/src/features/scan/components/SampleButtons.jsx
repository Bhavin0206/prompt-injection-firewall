import Button from "../../../components/common/Button";
import { SAMPLES } from "../data/samples";
import styles from "./SampleButtons.module.css";

// One-click demo buttons that load a SAFE or MALICIOUS sample into the input.
function SampleButtons({ onSelect, disabled = false }) {
  return (
    <div className={styles.row}>
      <span className={styles.label}>Try a sample:</span>
      <Button
        variant="secondary"
        size="sm"
        disabled={disabled}
        onClick={() => onSelect(SAMPLES.SAFE)}
      >
        ✓ Load SAFE example
      </Button>
      <Button
        variant="danger"
        size="sm"
        disabled={disabled}
        onClick={() => onSelect(SAMPLES.MALICIOUS)}
      >
        ✗ Load MALICIOUS example
      </Button>
    </div>
  );
}

export default SampleButtons;