// mode_manager.js — Penanganan Transisi Mode UI Kiosk & Barrier Indikator

class ModeManager {
  constructor(apiBaseUrl) {
    this.apiBaseUrl = apiBaseUrl;
    this.currentMode = "standby";
    this.avatarSection = document.getElementById("avatarSection");
    this.visualSection = document.getElementById("visualSection");
    this.loadingBarrier = document.getElementById("loadingBarrier");
    this.barrierText = document.getElementById("barrierText");
    this.currentModeBadge = document.getElementById("currentModeBadge");
  }

  async switchMode(targetMode) {
    console.log(`[ModeManager] Meminta transisi mode: ${this.currentMode} -> ${targetMode}`);
    this.showBarrier(`Menyiapkan mode ${targetMode}... Membebaskan alokasi VRAM`);

    try {
      const response = await fetch(`${this.apiBaseUrl}/api/v1/mode/switch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_mode: targetMode })
      });

      if (!response.ok) {
        throw new Error(`Gagal beralih mode. HTTP ${response.status}`);
      }

      const result = await response.json();
      console.log("[ModeManager] Transisi sukses:", result);
      this.currentMode = targetMode;
      this.applyUILayout(targetMode);
    } catch (error) {
      console.error("[ModeManager] Error perpindahan mode:", error);
      alert(`Gagal berganti mode: ${error.message}`);
    } finally {
      this.hideBarrier();
    }
  }

  applyUILayout(mode) {
    this.currentModeBadge.textContent = `Mode: ${mode.replace("_", " ").toUpperCase()}`;

    // Perbarui highlight tombol
    document.querySelectorAll(".kiosk-touch-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === mode);
    });

    if (mode === "conversation" || mode === "standby") {
      this.avatarSection.style.display = "flex";
      this.visualSection.style.display = "none";
    } else {
      this.avatarSection.style.display = "none";
      this.visualSection.style.display = "flex";
    }
  }

  showBarrier(message) {
    this.barrierText.textContent = message;
    this.loadingBarrier.style.display = "flex";
  }

  hideBarrier() {
    this.loadingBarrier.style.display = "none";
  }
}

window.ModeManager = ModeManager;
