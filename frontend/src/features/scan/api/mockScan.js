// Temporary MOCK of the backend /scan endpoint.
// Heuristic-based so the demo gives sensible verdicts before the real API exists.
// When the backend is ready: flip USE_MOCK off in ../api/scanApi.js and delete this file.

import { VERDICT, ATTACK_TYPES } from "../../../utils/constants";

// Lower-case, normalized content to match against.
const RULES = [
  {
    type: "Instruction Override",
    weight: 3,
    patterns: [
      "ignore all previous",
      "ignore previous",
      "disregard",
      "override",
      "forget all previous",
      "do not follow the instructions",
    ],
  },
  {
    type: "Secret Extraction",
    weight: 3,
    patterns: [
      "system prompt",
      "api key",
      "access token",
      "credentials",
      "secret",
      "confidential",
      "reveal",
      "extract",
      "print them in plain text",
    ],
  },
  {
    type: "Credential Theft",
    weight: 2,
    patterns: [
      "login",
      "session token",
      "admin password",
      "database credentials",
      "username and password",
      "log in as",
    ],
  },
  {
    type: "Role Change",
    weight: 2,
    patterns: [
      "you are now",
      "act as",
      "pretend to be",
      "behave as",
      "your new role",
      "administrative override mode",
    ],
  },
  {
    type: "Tool Abuse",
    weight: 2,
    patterns: [
      "run the command",
      "run this command",
      "execute",
      "payment terminal",
      "sql injection",
      "open a shell",
    ],
  },
  {
    type: "Encoded Instructions",
    weight: 2,
    patterns: [
      "base64",
      "rot13",
      "hex decode",
      "unicode escape",
      "leet",
      "caesar cipher",
    ],
  },
  {
    type: "Indirect Prompt Injection",
    weight: 2,
    patterns: [
      "hidden prompt",
      "embedded instruction",
      "ignore the text above",
      "this message is from the system",
      "inside the document",
    ],
  },
];

function detect(content) {
  const text = content.toLowerCase();

  let best = null;
  for (const rule of RULES) {
    let matches = 0;
    let firstPattern = null;
    for (const pattern of rule.patterns) {
      if (text.includes(pattern)) {
        matches += 1;
        firstPattern = firstPattern || pattern;
      }
    }
    if (matches === 0) continue;

    const score = rule.weight + matches;
    if (!best || score > best.score) {
      best = { ...rule, matches, score, firstPattern };
    }
  }
  return best;
}

// Simulate network latency so the loading spinner is visible.
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function mockScan(content) {
  const trimmed = String(content || "").trim();
  await delay(600 + Math.random() * 600);

  const hit = detect(trimmed);

  if (!hit) {
    return {
      verdict: VERDICT.SAFE,
      attackType: null,
      reason:
        "No prompt-injection patterns or suspicious instructions were found in the content.",
      confidence: 80 + Math.floor(Math.random() * 15), // 80-94
    };
  }

  return {
    verdict: VERDICT.BLOCKED,
    attackType: hit.type,
    reason: `Detected ${hit.type}: content matched suspicious pattern${
      hit.matches > 1 ? "s" : ""
    } (e.g. "${hit.firstPattern}").`,
    confidence: Math.min(99, 65 + (hit.score - 1) * 8 + Math.floor(Math.random() * 10)),
  };
}

// Export for potential reuse/debugging.
export { RULES, ATTACK_TYPES };