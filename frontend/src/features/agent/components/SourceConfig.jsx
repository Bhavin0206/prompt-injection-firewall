import { useState } from "react";
import Button from "../../../components/common/Button";
import styles from "./SourceConfig.module.css";

// Configure where the agent fetches content from.
// Either "use the bundled sample folder" OR add your own URL / folder sources.
function SourceConfig({
  sources,
  onChange,
  useSample,
  onUseSampleChange,
  disabled = false,
}) {
  const [url, setUrl] = useState("");
  const [folder, setFolder] = useState("");

  const addSource = (source) => {
    onChange([...sources, source]);
    onUseSampleChange(false);
  };

  const removeSource = (index) => {
    const next = sources.filter((_, i) => i !== index);
    onChange(next);
    if (next.length === 0) onUseSampleChange(true);
  };

  const addUrl = () => {
    const value = url.trim();
    if (!value) return;
    addSource({ type: "url", value });
    setUrl("");
  };

  const addFolder = () => {
    const value = folder.trim();
    if (!value) return;
    addSource({ type: "folder", value });
    setFolder("");
  };

  return (
    <div className={styles.wrapper}>
      <label className={styles.checkbox}>
        <input
          type="checkbox"
          checked={useSample}
          disabled={disabled}
          onChange={(event) => onUseSampleChange(event.target.checked)}
        />
        <span>
          Use the <strong>bundled sample folder</strong> (safe + malicious emails)
        </span>
      </label>

      <div className={`${styles.adders} ${useSample ? styles.muted : ""}`}>
        <div className={styles.inputRow}>
          <input
            type="text"
            className={styles.input}
            placeholder="https://example.com/article"
            value={url}
            disabled={disabled || useSample}
            onChange={(event) => setUrl(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && addUrl()}
          />
          <Button
            variant="secondary"
            onClick={addUrl}
            disabled={disabled || useSample || !url.trim()}
          >
            Add URL
          </Button>
        </div>

        <div className={styles.inputRow}>
          <input
            type="text"
            className={styles.input}
            placeholder="C:\path\to\a\folder"
            value={folder}
            disabled={disabled || useSample}
            onChange={(event) => setFolder(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && addFolder()}
          />
          <Button
            variant="secondary"
            onClick={addFolder}
            disabled={disabled || useSample || !folder.trim()}
          >
            Add folder
          </Button>
        </div>
      </div>

      {sources.length > 0 && (
        <ul className={styles.list}>
          {sources.map((source, index) => (
            <li key={`${source.type}-${source.value}-${index}`} className={styles.item}>
              <span className={styles.type}>{source.type}</span>
              <span className={styles.value} title={source.value}>
                {source.value}
              </span>
              <Button
                variant="ghost"
                size="sm"
                disabled={disabled}
                onClick={() => removeSource(index)}
              >
                Remove
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SourceConfig;
