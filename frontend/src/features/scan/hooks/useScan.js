import { useCallback, useRef, useState } from "react";
import { scanContent } from "../api/scanApi";

// Tracks the state of a scan call: the latest result, an error message,
// and a loading flag. runScan fires a scan; reset clears all state.
function useScan() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Stale-response guard: only the most recent runScan can update state.
  const seqRef = useRef(0);

  const runScan = useCallback(async (content) => {
    const trimmed = String(content || "").trim();
    if (!trimmed) {
      setError("Enter or upload some content before scanning.");
      return;
    }

    const seq = ++seqRef.current;
    setLoading(true);
    setError("");
    // Keep the previous verdict visible while a new scan is in flight.

    try {
      const res = await scanContent(trimmed);
      if (seq !== seqRef.current) return undefined; // a newer scan started
      setResult(res);
      return res;
    } catch (err) {
      if (seq !== seqRef.current) return undefined;
      setResult(null);
      setError(err?.message || "Scan failed. Please try again.");
      return null;
    } finally {
      if (seq === seqRef.current) setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    seqRef.current += 1;
    setResult(null);
    setError("");
    setLoading(false);
  }, []);

  return { result, error, loading, runScan, reset };
}

export default useScan;