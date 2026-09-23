import styles from "./Badge.module.css";

// Small pill label.
// variant: success | danger | warning | info | neutral
function Badge({ children, variant = "neutral", className = "" }) {
  return (
    <span className={`${styles.badge} ${styles[variant]} ${className}`}>
      {children}
    </span>
  );
}

export default Badge;
