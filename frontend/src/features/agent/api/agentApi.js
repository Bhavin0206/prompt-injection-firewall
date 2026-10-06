// Agent API — POST /api/agent/run
//
// Body: { sources: [{ type: "url" | "folder", value, label? }] }
// Empty sources -> the backend uses its bundled sample folder.

import { apiClient } from "../../../services/apiClient";

export async function runAgent(sources = []) {
  return apiClient.post("/api/agent/run", { sources });
}
