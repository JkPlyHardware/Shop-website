const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data.detail || data.error || data.message || Object.values(data).flat().join(" ") || "Request failed. Please try again.";
    throw new Error(message);
  }
  return data;
}

export const api = {
  products: (query = "") => request(`/products/${query}`),
  categories: () => request("/categories/"),
  campaigns: () => request("/campaigns/active/"),
  testimonials: () => request("/testimonials/"),
  contact: (payload, key) => request("/contact/", { method: "POST", body: JSON.stringify(payload), headers: { "Idempotency-Key": key } }),
  quote: (payload, key) => request("/quotes/", { method: "POST", body: JSON.stringify(payload), headers: { "Idempotency-Key": key } }),
  chat: (payload) => request("/chatbot/", { method: "POST", body: JSON.stringify(payload) }),
  campaignEvent: (id, event_type) => request(`/campaigns/${id}/event/`, { method: "POST", body: JSON.stringify({ event_type }) }),
};

export function makeIdempotencyKey() {
  return globalThis.crypto?.randomUUID?.() || `jk-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}
