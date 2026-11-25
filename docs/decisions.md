# DECISIONS.md — Log Keputusan Arsitektur dan Rekayasa

Dokumen ini mencatat keputusan-keputusan teknis penting, tanggal pengambilan keputusan, alternatif yang dipertimbangkan, alasan pemilihan, serta dampaknya terhadap sistem.

> **Hubungan Antar-Dokumen:**
> - Status progres pelaksanaan keputusan dilacak di [CHECKPOINT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/CHECKPOINT.md).
> - Panduan realisasi implementasi teknis berada di [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md).
> - Dampak keputusan terhadap metrik evaluasi dirujuk di [METRICS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/METRICS.md).
> - Konteks makro dan batasan penelitian dijelaskan pada [AGENT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/AGENT.md).

---

## Format Entri Keputusan
Setiap keputusan harus mencakup:
- **ID & Judul:** `ADR-xxx: Judul Keputusan`
- **Tanggal & Status:** Disetujui / Diusulkan / Ditinggalkan
- **Konteks & Masalah:** Masalah teknis yang dihadapi.
- **Alternatif yang Dipertimbangkan:** Pilihan lain beserta kelemahan/kelebihannya.
- **Keputusan:** Solusi yang dipilih.
- **Konsekuensi & Rationale:** Alasan ilmiah/rekayasa dan dampak lanjutan pada sistem/laporan.

---

## Log Keputusan (ADR)

### ADR-001: Pemilihan Web Application + Chromium Kiosk untuk UI Kiosk
- **Tanggal:** 30 September 2026 (Sesuai PoC rev. A)
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** Antarmuka kiosk memerlukan tampilan potret fullscreen (9:16) pada layar sentuh 32 inci yang terhubung ke Ubuntu Linux, dengan kemampuan rendering cepat untuk status percakapan, video streaming, dan galeri citra.
- **Alternatif:**
  1. *Flutter Desktop (Linux):* Pernah diusulkan dalam draf awal, tetapi memiliki dependensi pustaka native Wayland/X11 yang lebih rentan konflik dengan driver grafis, integrasi WebRTC/video streaming lebih kompleks, dan fleksibilitas penyesuaian layout potret lebih rendah dibanding web modern.
  2. *Web Application (HTML/CSS/JS) via Chromium Kiosk Mode:* Stack resmi yang disepakati pada PoC.
- **Keputusan:** Menggunakan Web Application modern yang dijalankan pada Chromium fullscreen kiosk mode (`chromium-browser --kiosk`).
- **Konsekuensi:** Frontend terpisah secara bersih dari backend via REST/WebSocket, mempermudah inspeksi antarmuka dan penanganan transisi antar-layanan.

---

### ADR-002: Lingkup Orkestrasi pada Level Proses/Aplikasi (Bukan Kernel GPU)
- **Tanggal:** 29 Oktober 2026
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** Mesin smart kiosk memiliki 1 GPU fisik NVIDIA RTX 5060 dengan VRAM terbatas (8 GB). Perlu penegasan batas kontribusi tugas akhir di bidang Teknik Komputer.
- **Alternatif:**
  1. *Kernel-level GPU Scheduling / GPU Virtualization (vGPU / MIG):* Membutuhkan GPU kelas data center (A100/H100) dan modifikasi driver kernel yang di luar batas realistis hardware kelas konsumen RTX 5060.
  2. *Application-level Lifecycle Orchestration:* Membangun orkestrator yang mengelola siklus hidup model (`load`, `unload`, `health`, `readiness timeout`) dan kebijakan alokasi mode eksklusif.
- **Keputusan:** Mengambil pendekatan Application-level Lifecycle & Resource-Aware Orchestration.
- **Konsekuensi:** Laporan TA tidak boleh mengklaim modifikasi driver kernel atau jaminan pemartisian keras VRAM, melainkan mengevaluasi efektivitas lifecycle management pada level aplikasi.

---

### ADR-003: Protokol Komunikasi Gateway & Orkestrator (REST + WebSocket)
- **Tanggal:** 29 Oktober 2026
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** Antarmuka kiosk memerlukan permintaan aksi diskrit (seperti switch mode, aktivasi layanan) sekaligus streaming pembaruan status real-time (loading progres, VRAM live usage, token percakapan).
- **Alternatif:**
  1. *Pure REST Polling:* Membebani gateway dengan request berulang untuk memeriksa kesiapan model (`readiness`).
  2. *gRPC:* Kinerja tinggi namun membutuhkan setup tooling protobuf di sisi frontend web dan debugging network browser lebih rumit.
  3. *Kombinasi REST API + WebSocket:* REST untuk kontrol diskrit (`POST /activate`, `POST /load`), WebSocket untuk push event asinkronus (streaming status, latency logs).
- **Keputusan:** Menggunakan kombinasi FastAPI REST API dan WebSocket.
- **Konsekuensi:** UI dapat merespons perubahan status kesiapan model secara instan tanpa polling konstan.

---

### ADR-004: Penanganan Mode Eksklusif untuk Fitur Citra & Video Berat
- **Tanggal:** 29 Oktober 2026
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** Fitur Try-On Video (Erdi) dan AI Photobooth (Deva) membutuhkan alokasi VRAM besar yang mendekati kapasitas maksimum 8 GB, sehingga tidak dapat berjalan bersamaan dengan pipeline percakapan.
- **Alternatif:**
  1. *Membiarkan model tetap resident:* Menyebabkan *CUDA Out of Memory* (OOM) fatal saat model kedua dipanggil.
  2. *Graceful Unload & Barrier Switch:* Orkestrator secara eksplisit memerintahkan unload seluruh model percakapan, memverifikasi pembebasan VRAM via NVML, baru memicu pemuatan model eksklusif.
- **Keputusan:** Menerapkan Exclusive GPU Mode dengan mekanisme barrier state (`STOPPING` -> verifikasi VRAM turun -> `STARTING` layanan target).
- **Konsekuensi:** Waktu perpindahan antar-mode akan bertambah sebesar durasi unload + load, yang harus dicatat dan dianalisis dalam Bab IV sebagai trade-off kestabilan.

---

### ADR-005: Validasi Mandiri Strategi C (Pinned-Memory Swap) dan D (Prefetch)
- **Tanggal:** 29 Oktober 2026
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** PoC mengusulkan empat strategi (A: All-resident, B: Naive load/unload, C: Pinned-memory swap, D: Prefetch). Namun tidak semua runtime model (Ollama / llama.cpp / PyTorch) mendukung pinned host-memory swap secara out-of-the-box.
- **Alternatif:**
  1. *Mensimulasikan swap pinned memory dengan load disk dan mengklaimnya sebagai Strategi C:* Menyesatkan secara ilmiah dan melanggar integritas akademik.
  2. *Menguji kelayakan runtime pada M0, jika tidak didukung catat sebagai batasan sistem:* Hanya laporkan strategi yang implementasi fisiknya benar-benar bekerja.
- **Keputusan:** Strategi C hanya diuji jika runtime model yang dipilih secara sah menyediakan API pinned memory; jika tidak ada, dicatat secara transparan sebagai batasan runtime.
- **Konsekuensi:** Validitas ilmiah laporan Bab IV terjamin dari klaim palsu.

### ADR-006: UI Kiosk Vanilla JavaScript Terintegrasi dengan Gateway FastAPI yang Ada
- **Tanggal:** 25 November 2026
- **Status:** `DISETUJUI`
- **Konteks & Masalah:** UI M4 memerlukan navigasi empat layanan, status readiness, dan mode simulasi, sementara gateway yang sudah berjalan di repositori adalah FastAPI dan registry layanan telah memakai `configs/services.yaml`.
- **Alternatif:** Menambahkan backend Express terpisah seperti brief prototipe; mengganti gateway yang telah menjadi bagian dari kontribusi orkestrator; atau mempertahankan FastAPI dan menambahkan facade REST tipis untuk kontrak UI.
- **Keputusan:** Mempertahankan gateway FastAPI yang ada dan membangun UI dengan Vanilla JavaScript ES modules. Facade UI memetakan ID pengalaman ke layanan registry, memisahkan jawaban simulasi dari jalur inference adapter, serta menunggu `/health` READY sebelum inference pada mode nyata.
- **Konsekuensi & Rationale:** Tidak ada service backend kedua yang mengaburkan arsitektur atau mengganggu target Linux. Empat pengalaman tetap terpisah pada level adapter; konfigurasi mock dan timeout diberikan melalui environment.