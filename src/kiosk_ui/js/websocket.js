// websocket.js — Real-Time WebSocket Telemetry & Event Listener

class KioskWebSocketClient {
  constructor(url, onMessageCallback, onStatusCallback) {
    this.url = url;
    this.onMessage = onMessageCallback;
    this.onStatus = onStatusCallback;
    this.socket = null;
    this.reconnectInterval = 3000;
  }

  connect() {
    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        if (this.onStatus) this.onStatus(true);
        console.log("[WS] Terhubung ke Orchestrator Gateway.");
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.onMessage) this.onMessage(data);
        } catch (e) {
          console.error("[WS] Gagal mem-parsing payload JSON:", e);
        }
      };

      this.socket.onclose = () => {
        if (this.onStatus) this.onStatus(false);
        console.warn("[WS] Sambungan terputus. Mencoba reconnect dalam 3s...");
        setTimeout(() => this.connect(), this.reconnectInterval);
      };

      this.socket.onerror = (err) => {
        console.error("[WS] Error sambungan:", err);
        this.socket.close();
      };
    } catch (e) {
      console.error("[WS] Inisialisasi socket gagal:", e);
    }
  }

  send(payload) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(payload));
    }
  }
}

window.KioskWebSocketClient = KioskWebSocketClient;
