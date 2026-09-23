import styles from "./Spinner.module.css";

// Small loading spinner. Inherits its color from the parent (currentColor).
function Spinner({ size = "md", label = "Loading", className = "" }) {
  return (
    <span
      className={`${styles.spinner} ${styles[size]} ${className}`}
      role="status"
      aria-label={label}
    />
  );
}

export default Spinner;
