import { useState } from "react";
import PageLayout from "./components/layout/PageLayout";
import ScanPage from "./pages/ScanPage";
import AgentPage from "./pages/AgentPage";
import { MODES } from "./utils/constants";

function App() {
  const [mode, setMode] = useState(MODES.MANUAL);

  return (
    <PageLayout mode={mode} onModeChange={setMode}>
      {mode === MODES.MANUAL ? <ScanPage /> : <AgentPage />}
    </PageLayout>
  );
}

export default App;
