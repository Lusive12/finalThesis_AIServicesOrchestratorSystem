const config = window.KIOSK_CONFIG || {};
const API_BASE = (config.apiBase || `${location.protocol}//${location.host}`).replace(/\/$/, "");

async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout || 12000);
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: { "Content-Type": "application/json", ...(options.headers || {}) }
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || `Permintaan gagal (${response.status})`);
    return data;
  } catch (error) {
    if (error.name === "AbortError") throw new Error("Layanan terlalu lama merespons. Silakan coba lagi.");
    throw error;
  } finally { clearTimeout(timeout); }
}

export const api = {
  config: () => request("/api/kiosk-config"),
  services: () => request("/api/services"),
  status: id => request(`/api/services/${encodeURIComponent(id)}/status`),
  start: id => request(`/api/services/${encodeURIComponent(id)}/start`, { method: "POST", body: "{}" }),
  stop: id => request(`/api/services/${encodeURIComponent(id)}/stop`, { method: "POST", body: "{}" }),
  health: id => request(`/api/services/${encodeURIComponent(id)}/health`),
  infer: (id, payload) => request(`/api/services/${encodeURIComponent(id)}/infer`, { method: "POST", body: JSON.stringify(payload), timeout: 90000 })
};
