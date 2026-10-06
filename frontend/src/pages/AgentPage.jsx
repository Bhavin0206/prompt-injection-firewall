import { useState } from "react";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import SourceConfig from "../features/agent/components/SourceConfig";
import AgentStatus from "../features/agent/components/AgentStatus";
import AgentResults from "../features/agent/components/AgentResults";
import useAgentRun from "../features/agent/hooks/useAgentRun";
import styles from "./AgentPage.module.css";

// Mode B (Way 2): the autonomous agent fetches content from sources and the
// firewall scans every item automatically.
function AgentPage() {
  const [sources, setSources] = useState([]);
  const [useSample, setUseSample] = useState(true);
  const { result, error, loading, run } = useAgentRun();

  const canRun = useSample || sources.length > 0;
  const handleRun = () => run(useSample ? [] : sources);

  return (
    <div className={styles.page}>
      <header className={styles.pageHeader}>
        <h2 className={styles.title}>Autonomous Agent</h2>
        <p className={styles.subtitle}>
          The agent fetches content from your sources and the firewall scans
          every item automatically — nothing reaches the AI unless it is safe.
        </p>
      </header>

      <Card title="Sources">
        <SourceConfig
          sources={sources}
          onChange={setSources}
          useSample={useSample}
          onUseSampleChange={setUseSample}
          disabled={loading}
        />

        <div className={styles.runRow}>
          <Button size="lg" loading={loading} onClick={handleRun} disabled={!canRun}>
            {loading ? "Agent running..." : "Run Agent"}
          </Button>
          <span className={styles.runHint}>
            {useSample
              ? "Using the bundled sample folder"
              : `${sources.length} source${sources.length === 1 ? "" : "s"}`}
          </span>
        </div>

        <AgentStatus loading={loading} />
      </Card>

      {error && (
        <p className={styles.error} role="alert">
          {error}
        </p>
      )}

      {result && (
        <AgentResults
          summary={result.summary}
          results={result.results}
          errors={result.errors}
        />
      )}
    </div>
  );
}

export default AgentPage;
