import { useCallback, useState } from "react";
import ScanInput from "../features/scan/components/ScanInput";
import FileUpload from "../features/scan/components/FileUpload";
import SampleButtons from "../features/scan/components/SampleButtons";
import VerdictCard from "../features/scan/components/VerdictCard";
import ScanStatus from "../features/scan/components/ScanStatus";
import ScanLog from "../features/scan/components/ScanLog";
import useScan from "../features/scan/hooks/useScan";
import styles from "./ScanPage.module.css";

// Mode A (Manual): input + upload + samples in, verdict + history out.
function ScanPage() {
  const [content, setContent] = useState("");
  const [log, setLog] = useState([]);
  const [selectedEntry, setSelectedEntry] = useState(null);

  const { result, error, loading, runScan } = useScan();

  // Show a clicked history entry, otherwise the latest scan result.
  const displayed = selectedEntry ?? result;

  // Typing, uploading, or loading a sample drops any history selection.
  const handleContentChange = useCallback((value) => {
    setContent(value);
    setSelectedEntry(null);
  }, []);

  const appendLog = useCallback((res) => {
    setLog((prev) => [
      {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        at: new Date(),
        ...res,
      },
      ...prev,
    ]);
  }, []);

  const handleScan = useCallback(async () => {
    const res = await runScan(content);
    if (res) appendLog(res);
    setSelectedEntry(null);
  }, [content, runScan, appendLog]);

  return (
    <div className={styles.page}>
      <header className={`${styles.pageHeader} mb-1`}>
        <h2 className="text-xl font-semibold tracking-tight">Manual Scan</h2>
        <p className="mt-1 text-sm text-muted">
          Paste content, upload a file (text, PDF, email, or source code), or load a
          sample — then hit{" "}
          <span className="font-semibold text-primary">Scan</span>.
        </p>
      </header>

      <div className={styles.mainCol}>
        <ScanInput
          value={content}
          onChange={handleContentChange}
          onScan={handleScan}
          loading={loading}
        />

        <SampleButtons
          disabled={loading}
          onSelect={(sample) => handleContentChange(sample.content)}
        />

        <FileUpload
          disabled={loading}
          onFileRead={(fileContent) => handleContentChange(fileContent)}
        />

        <ScanStatus loading={loading} error={error} />

        <VerdictCard result={displayed} />
      </div>

      <aside className={styles.sideCol}>
        <ScanLog
          entries={log}
          onSelect={(entry) => setSelectedEntry(entry)}
        />
      </aside>
    </div>
  );
}

export default ScanPage;