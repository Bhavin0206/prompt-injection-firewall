import styles from "./Card.module.css";

// Simple surface container with an optional title.
function Card({ title, children, className = "" }) {
  return (
    <section className={`${styles.card} ${className}`}>
      {title && <h2 className={styles.title}>{title}</h2>}
      {children}
    </section>
  );
}

export default Card;
