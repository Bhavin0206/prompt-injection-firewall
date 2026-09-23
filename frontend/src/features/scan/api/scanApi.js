// Scan API — POST /scan.
// While the backend doesn't exist yet, USE_MOCK = true routes to the
// heuristic mock. One change (false) swaps to the real endpoint.

import { apiClient } from "../../../services/apiClient";
import { mockScan } from "./mockScan";

const USE_MOCK = true;

// POST /scan  { content }  ->  { verdict, attackType, reason, confidence }
export async function scanContent(content) {
  if (USE_MOCK) {
    return mockScan(content);
  }
  return apiClient.post("/scan", { content });
}

export { USE_MOCK };