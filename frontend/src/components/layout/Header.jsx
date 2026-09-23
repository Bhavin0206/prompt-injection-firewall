import { MODES } from "../../utils/constants";
import { useTheme } from "../../context/ThemeContext";
import styles from "./Header.module.css";

// App header: brand + Mode A / Mode B toggle + theme toggle.
// The mode toggle works now; the real Mode A / Mode B views are wired in Task 12.
function Header({ mode, onModeChange }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <span className={styles.logo} aria-hidden="true">
          🛡️
        </span>
        <h1 className={styles.title}>Prompt Injection Firewall</h1>
      </div>

      <div className={styles.actions}>
        <div className={styles.modeToggle} role="tablist" aria-label="Mode">
          <button
            type="button"
            role="tab"
            aria-selected={mode === MODES.MANUAL}
            className={`${styles.modeButton} ${
              mode === MODES.MANUAL ? styles.active : ""
            }`}
            onClick={() => onModeChange(MODES.MANUAL)}
          >
            Mode A · Manual
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={mode === MODES.AGENT}
            className={`${styles.modeButton} ${
              mode === MODES.AGENT ? styles.active : ""
            }`}
            onClick={() => onModeChange(MODES.AGENT)}
          >
            Mode B · Agent
          </button>
        </div>

        <button
          type="button"
          className={styles.themeButton}
          onClick={toggleTheme}
          aria-label="Toggle light and dark theme"
          title={theme === "dark" ? "Switch to light" : "Switch to dark"}
        >
          {theme === "dark" ? "☀️" : "🌙"}
        </button>
      </div>
    </header>
  );
}

export default Header;
