// Thin HTTP wrapper around fetch — the single place that talks to the backend.
import { config } from "../config";

// Turn a non-OK response into a friendly Error message.
async function readError(response) {
  try {
    const body = await response.json();
    const detail = body?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length) {
      return detail
        .map((item) => item.message || item.msg || "invalid input")
        .join("; ");
    }
    if (typeof body?.error === "string") return body.error.replace(/_/g, " ");
  } catch {
    // fall through to the generic message
  }
  return `Request failed (${response.status})`;
}

async function request(path, options = {}) {
  const response = await fetch(`${config.apiBaseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(await readError(response));
  }
  return response.json();
}

export const apiClient = {
  get: (path) => request(path),
  post: (path, body) =>
    request(path, { method: "POST", body: JSON.stringify(body) }),
};
