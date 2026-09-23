import Header from "./Header";
import styles from "./PageLayout.module.css";

// Page shell: header on top, page content in the middle.
function PageLayout({ mode, onModeChange, children }) {
  return (
    <div className={styles.layout}>
      <Header mode={mode} onModeChange={onModeChange} />
      <main className={styles.main}>{children}</main>
    </div>
  );
}

export default PageLayout;
