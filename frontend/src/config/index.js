// Central app configuration.
// Reads Vite environment variables (must start with VITE_).

export const config = {
  appName: "Prompt Injection Firewall",
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
};
