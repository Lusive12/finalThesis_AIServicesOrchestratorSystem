// app.js — Main Kiosk UI Entry Point & Event Wiring

document.addEventListener("DOMContentLoaded", () => {
  const host = window.location.hostname || "127.0.0.1";
  const port = "8000";
  const apiBaseUrl = `http://${host}:${port}`;
  const wsUrl = `ws://${host}:${port}/ws/events`;

  const vramTelemetry = document.getElementById("vramTelemetry");
  const wsStatus = document.getElementById("wsStatus");
  const transcriptText = document.getElementById("transcriptText");

  // Inisialisasi Mode Manager
  const modeManager = new window.ModeManager(apiBaseUrl);

  // Inisialisasi WebSocket Client
  const wsClient = new window.KioskWebSocketClient(
    wsUrl,
    (data) => {
      // Penanganan event telemetri & status
      if (data.event_type === "TELEMETRY_UPDATE") {
        vramTelemetry.textContent = `VRAM: ${data.vram_used_mb} / ${data.vram_total_mb} MB`;
      } else if (data.event_type === "TRANSCRIPT_UPDATE") {
        transcriptText.textContent = data.text;
      }
    },
    (isConnected) => {
      if (isConnected) {
        wsStatus.textContent = "Online";
        wsStatus.className = "ws-status-indicator connected";
      } else {
        wsStatus.textContent = "Offline";
        wsStatus.className = "ws-status-indicator";
      }
    }
  );

  wsClient.connect();

  // Pasang event listener ke tombol sentuh
  document.querySelectorAll(".kiosk-touch-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetMode = btn.dataset.mode;
      modeManager.switchMode(targetMode);
    });
  });

  console.log("[Kiosk App] Inisialisasi selesai.");
});
