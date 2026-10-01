// Scan API — POST /api/scan on the firewall backend.
//
//   USE_MOCK = true  -> use the local heuristic mock (no backend needed)
//   USE_MOCK = false -> call the real backend endpoint

import { apiClient } from "../../../services/apiClient";
import { mockScan } from "./mockScan";

const USE_MOCK = false;

// POST /api/scan  { content, source }
//   -> { verdict, attackType, reason, confidence }
export async function scanContent(content, source = "text") {
  if (USE_MOCK) {
    return mockScan(content);
  }
  return apiClient.post("/api/scan", { content, source });
}

export { USE_MOCK };
