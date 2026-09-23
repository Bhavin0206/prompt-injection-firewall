import styles from "./TextArea.module.css";

// Labelled textarea — used as the main content input for scanning.
function TextArea({
  id,
  label,
  value,
  onChange,
  placeholder,
  rows = 6,
  disabled = false,
  className = "",
  ...rest
}) {
  return (
    <div className={styles.field}>
      {label && (
        <label htmlFor={id} className={styles.label}>
          {label}
        </label>
      )}
      <textarea
        id={id}
        className={`${styles.textarea} ${className}`}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        disabled={disabled}
        {...rest}
      />
    </div>
  );
}

export default TextArea;
