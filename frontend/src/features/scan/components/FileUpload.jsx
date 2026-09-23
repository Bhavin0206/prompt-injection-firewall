import { useRef, useState } from "react";
import Card from "../../../components/common/Card";
import Spinner from "../../../components/common/Spinner";
import Button from "../../../components/common/Button";
import { readFileContent, isSupportedFile } from "../../../utils/readFileContent";
import styles from "./FileUpload.module.css";

// Accepted file types shown in the picker.
const ACCEPT =
  ".txt,.md,.csv,.tsv,.log,.json,.xml,.html,.htm,.yaml,.yml," +
  ".pdf,.eml," +
  ".js,.jsx,.ts,.tsx,.py,.java,.c,.h,.cpp,.cc,.cs,.go,.rs,.php,.rb,.sh,.bash,.sql,.r,.kt,.swift,.m";

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// Drop zone that reads text / PDF / email / source code files as text,
// fully client-side, then hands the content to onFileRead.
function FileUpload({ onFileRead, onError, disabled = false }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [reading, setReading] = useState(false);
  const [error, setError] = useState("");

  const openPicker = () => {
    if (disabled || reading) return;
    inputRef.current?.click();
  };

  const handleFiles = async (files) => {
    const picked = files?.[0];
    if (!picked || disabled || reading) return;

    setError("");
    setReading(true);
    try {
      const content = await readFileContent(picked);
      setFile(picked);
      onFileRead(content, picked);
    } catch (err) {
      setFile(null);
      setError(err.message);
      onError?.(err.message);
    } finally {
      setReading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (disabled || reading) return;
    const dropped = Array.from(e.dataTransfer.files);
    if (dropped.length > 0 && !isSupportedFile(dropped[0])) {
      setError(`"${dropped[0].name}" is not a supported file type.`);
      onError?.(`"${dropped[0].name}" is not a supported file type.`);
      return;
    }
    handleFiles(dropped);
  };

  return (
    <Card title="Upload a File">
      <div className={styles.container}>
        <div
          className={`${styles.dropzone} ${disabled || reading ? styles.disabled : ""}`}
          role="button"
          tabIndex={0}
          aria-label="Upload or drag a file to scan"
          onClick={openPicker}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              openPicker();
            }
          }}
          onDragOver={(e) => {
            e.preventDefault();
            if (!disabled && !reading) e.currentTarget.classList.add(styles.dragging);
          }}
          onDragLeave={(e) => e.currentTarget.classList.remove(styles.dragging)}
          onDrop={handleDrop}
        >
          <input
            ref={inputRef}
            type="file"
            className={styles.input}
            accept={ACCEPT}
            disabled={disabled || reading}
            onChange={(e) => handleFiles(e.target.files)}
          />

          <span className={styles.icon} aria-hidden="true">
            🗂️
          </span>

          {reading ? (
            <div className={styles.reading}>
              <Spinner size="sm" />
              <span className={styles.readingText}>Reading {file ? file.name : "file"}…</span>
            </div>
          ) : (
            <>
              <p className={styles.title}>Click to choose or drag &amp; drop</p>
              <p className={styles.hint}>
                Text · PDF · Email (.eml) · Source code — read in your browser, file
                never leaves your machine.
              </p>
            </>
          )}
        </div>

        {file && !error && (
          <div className={styles.fileRow}>
            <span className={styles.fileName} title={file.name}>
              {file.name}
            </span>
            <span className={styles.fileSize}>{formatSize(file.size)}</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setFile(null);
                setError("");
              }}
              disabled={reading}
            >
              Clear
            </Button>
          </div>
        )}

        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
      </div>
    </Card>
  );
}

export default FileUpload;