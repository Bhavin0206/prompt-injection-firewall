import { useCallback, useState } from "react";
import { runAgent } from "../api/agentApi";

// Tracks one agent run: result (summary + results), error and loading.
function useAgentRun() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const run = useCallback(async (sources = []) => {
    setLoading(true);
    setError("");
    try {
      const res = await runAgent(sources);
      setResult(res);
      return res;
    } catch (err) {
      setResult(null);
      setError(err?.message || "Agent run failed. Please try again.");
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError("");
    setLoading(false);
  }, []);

  return { result, error, loading, run, reset };
}

export default useAgentRun;
