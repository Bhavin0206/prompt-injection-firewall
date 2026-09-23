// Shared constants used across the app.

export const VERDICT = {
  SAFE: "safe",
  BLOCKED: "blocked",
};

// The 9 attack types from the problem statement.
export const ATTACK_TYPES = [
  "Instruction Override",
  "Role Change",
  "Secret Extraction",
  "Tool Abuse",
  "Credential Theft",
  "Context Poisoning",
  "Multi-Step Jailbreaks",
  "Encoded Instructions",
  "Indirect Prompt Injection",
];

// The two modes of the app.
export const MODES = {
  MANUAL: "manual", // Mode A (Way 1)
  AGENT: "agent", // Mode B (Way 2)
};

// Content sources the user can submit.
export const SOURCES = {
  TEXT: "text",
  WEB: "web",
  EMAIL: "email",
  PDF: "pdf",
  IMAGE: "image",
  API: "api",
  CODE: "code",
};
