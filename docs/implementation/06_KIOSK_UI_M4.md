# 06_KIOSK_UI_M4.md — Implementasi Antarmuka Web Kiosk & Integrasi Chromium (Milestone M4)

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Milestone M4 (Tugas Besar 1: UI/UX Chromium Kiosk)  
> **Target:** Web Application Portrait 9:16, WebSocket Client, Display Server Kiosk Script

---

## 1. Tujuan Dokumen
1. Membangun antarmuka pengguna kios (*Kiosk User Interface*) berbasis web modern (HTML5, Vanilla CSS, dan JavaScript).
2. Mengadopsi tata letak potret berasio **9:16 (1080 × 1920 piksel)** untuk layar sentuh 32 inci.
3. Mengintegrasikan klien WebSocket dua arah untuk memantau status model secara instan (*real-time status streaming*).
4. Menyediakan skrip peluncuran otomatis peramban Chromium dalam mode layar penuh (*fullscreen kiosk mode*).

---

## 2. Struktur Antarmuka Web Kiosk (`src/ui/`)

```text
src/ui/
├── index.html         # Struktur tampilan potret & layout container
├── css/
│   └── kiosk.css      # Desain grafis modern (glassmorphism, anim transition)
└── js/
    ├── app.js         # Logika interaksi, event sentuhan, & router tampilan
    └── websocket.js   # Penghubung WebSocket ke Orchestrator
```

---

## 3. Implementasi Kode Web Kiosk

### 3.1 Berkas `src/ui/index.html`
```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0, user-scalable=no">
  <title>Smart Kiosk AI Assistant</title>
  <link rel="stylesheet" href="css/kiosk.css">
</head>
<body>
  <div id="kiosk-container">
    <!-- Header Status Kiosk -->
    <header class="kiosk-header">
      <div class="logo-area">
        <h1>SMART KIOSK</h1>
        <p class="subtitle">Multi-AI Service Assistant</p>
      </div>
      <div class="system-badge" id="vram-badge">
        <span class="dot live"></span> VRAM: <span id="vram-text">Loading...</span>
      </div>
    </header>

    <!-- View 1: Layar Standby & Menu Utama -->
    <section id="view-standby" class="view active">
      <div class="welcome-box">
        <h2>Selamat Datang</h2>
        <p>Sentuh salah satu layanan di bawah untuk memulai</p>
      </div>
      <div class="services-grid">
        <button class="service-card" onclick="triggerService('speech_pipeline')">
          <div class="card-icon">🎙️</div>
          <h3>Percakapan Suara</h3>
          <p>Tanya jawab interaktif asisten</p>
        </button>
        <button class="service-card" onclick="triggerService('fashion_recommendation')">
          <div class="card-icon">👗</div>
          <h3>Rekomendasi Busana</h3>
          <p>Analisis gaya berbasis visi AI</p>
        </button>
        <button class="service-card" onclick="triggerService('virtual_tryon')">
          <div class="card-icon">🪞</div>
          <h3>Virtual Try-On</h3>
          <p>Fitting pakaian virtual langsung</p>
        </button>
        <button class="service-card" onclick="triggerService('photobooth')">
          <div class="card-icon">📸</div>
          <h3>AI Photobooth</h3>
          <p>Kreasi potret artistik</p>
        </button>
      </div>
    </section>

    <!-- View 2: Layar Loading Transisi -->
    <section id="view-loading" class="view">
      <div class="loader-box">
        <div class="spinner"></div>
        <h3 id="loading-title">Menyiapkan Layanan...</h3>
        <p id="loading-desc">Orkestrator sedang mengatur alokasi memori GPU</p>
      </div>
    </section>

    <!-- View 3: Layar Interaksi Aktif -->
    <section id="view-active" class="view">
      <div class="active-header">
        <h2 id="active-service-title">Layanan Aktif</h2>
        <button class="btn-back" onclick="returnToStandby()">Kembali ke Menu</button>
      </div>
      <div id="interaction-content" class="active-content">
        <!-- Konten dinamis dirender di sini via app.js -->
      </div>
    </section>
  </div>

  <script src="js/websocket.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
```

### 3.2 Berkas `src/ui/css/kiosk.css` (Gaya Potret 9:16 Modern)
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  user-select: none;
}

body {
  width: 1080px;
  height: 1920px;
  background: #0f172a;
  color: #f8fafc;
  overflow: hidden;
}

#kiosk-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 60px 40px;
}

.kiosk-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #1e293b;
  padding-bottom: 30px;
}

.logo-area h1 {
  font-size: 42px;
  letter-spacing: 2px;
  color: #38bdf8;
}

.system-badge {
  background: #1e293b;
  padding: 12px 24px;
  border-radius: 20px;
  font-size: 20px;
}

.view {
  display: none;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.view.active {
  display: flex;
}

.services-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
  max-width: 960px;
  margin-top: 60px;
}

.service-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 24px;
  padding: 50px 30px;
  text-align: center;
  color: #fff;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.service-card:active {
  transform: scale(0.96);
  border-color: #38bdf8;
}

.card-icon {
  font-size: 72px;
  margin-bottom: 20px;
}

.spinner {
  width: 80px;
  height: 80px;
  border: 8px solid #334155;
  border-top: 8px solid #38bdf8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 30px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

### 3.3 Berkas `src/ui/js/websocket.js` (Integrasi Real-time)
```javascript
const GATEWAY_WS_URL = "ws://127.0.0.1:8000/ws/status";
const GATEWAY_HTTP_URL = "http://127.0.0.1:8000";

let ws = null;

function initWebSocket() {
  ws = new WebSocket(GATEWAY_WS_URL);

  ws.onopen = () => {
    console.log("Connected to Orchestrator WebSocket");
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    handleServerEvent(msg);
  };

  ws.onclose = () => {
    console.warn("WebSocket disconnected. Reconnecting in 2s...");
    setTimeout(initWebSocket, 2000);
  };
}

function handleServerEvent(msg) {
  if (msg.event === "STATE_CHANGE") {
    const { service, state } = msg.data;
    if (state === "READY") {
      onServiceReady(service);
    } else if (state === "ERROR") {
      onServiceError(service, msg.data.error);
    }
  }
}

async function triggerService(serviceId) {
  showView("view-loading");
  try {
    const res = await fetch(`${GATEWAY_HTTP_URL}/services/${serviceId}/activate`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Aktivasi gagal");
  } catch (err) {
    onServiceError(serviceId, err.message);
  }
}

initWebSocket();
```

---

## 4. Skrip Peluncuran Otomatis Chromium Kiosk (`scripts/launch_kiosk.sh`)

Simpan skrip peluncuran ini pada `scripts/launch_kiosk.sh`:

```bash
#!/bin/bash
# Matikan screen saver dan manajemen daya monitor
xset s noblank
xset s off
xset -dpms

# Sembunyikan kursor kursor mouse
unclutter -idle 0.5 -root &

# Pastikan rotasi layar sentuh telah disetel ke potret
xrandr --output HDMI-1 --rotate right

# Buka Chromium dalam mode fullscreen kiosk murni
chromium-browser \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --check-for-update-interval=31536000 \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --app="file:///$(pwd)/src/ui/index.html"
```

Beri izin eksekusi:
```bash
chmod +x scripts/launch_kiosk.sh
```

---

## 5. Kriteria Keberhasilan Milestone M4
- [ ] Antarmuka web berhasil memenuhi layar 1080 × 1920 tanpa scrollbar atau URL address bar.
- [ ] Tombol menu sentuh merespons secara mulus tanpa penundaan.
- [ ] Transisi status dari Standby $\rightarrow$ Loading $\rightarrow$ Active berlangsung otomatis berdasarkan event WebSocket dari backend.
