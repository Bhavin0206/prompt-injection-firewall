import { useState } from "react";
import PageLayout from "./components/layout/PageLayout";
import ScanPage from "./pages/ScanPage";
import { MODES } from "./utils/constants";

function App() {
  const [mode, setMode] = useState(MODES.MANUAL);

  return (
    <PageLayout mode={mode} onModeChange={setMode}>
      {mode === MODES.MANUAL ? (
        <ScanPage />
      ) : (
        <p className="app-subtitle px-4 py-10 text-center text-muted">
          Mode B (Agent) — UI coming later.
        </p>
      )}
    </PageLayout>
  );
}

export default App;
