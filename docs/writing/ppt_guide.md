---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Poppins', 'Calibri', 'Segoe UI', sans-serif;
    color: #1e293b;
    background-color: #f8fafc;
    padding: 35px 50px;
  }
  h1 {
    font-family: 'Poppins', sans-serif;
    color: #0f172a;
    font-weight: 700;
  }
  h2 {
    font-family: 'Poppins', sans-serif;
    color: #0284c7;
    font-weight: 600;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 8px;
  }
  h3 {
    font-family: 'Poppins', sans-serif;
    color: #334155;
    font-weight: 600;
  }
  strong {
    color: #0369a1;
  }
  .highlight-card {
    background-color: #ffffff;
    border-left: 5px solid #0284c7;
    padding: 12px 18px;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    margin-bottom: 12px;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
  }
  .table-slide {
    font-size: 0.82em;
  }
  .badge {
    background: #e0f2fe;
    color: #0369a1;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.78em;
  }
---

<!-- 
SLIDE 1: COVER / JUDUL PRESENTASI
Rekomendasi Font: Poppins (Heading) & Calibri / Inter (Body)
Gaya Visual: Clean, Modern Academic Executive, Dark Navy Accent
-->

# SISTEM ORKESTRASI LAYANAN AI BERBASIS MICROSERVICES PADA SISTEM SMART KIOSK

### Seminar Proposal / Progress Tugas Akhir — Teknik Komputer FTEIC ITS

---

<div class="highlight-card">

**Penyusun:**
- **Nama Mahasiswa:** Rendy Lexxy Kurniawan
- **NRP:** 5024231007
- **Departemen:** Teknik Komputer, Fakultas Teknik Elektro dan Informatika Cerdas (FTEIC)
- **Institusi:** Institut Teknologi Sepuluh Nopember (ITS) Surabaya

**Dosen Pembimbing:**
- **Dosen Pembimbing:** Arta Kusuma Hernanda, S.T., M.T. *(NIP. 1996202311024)*
- **Dosen Ko-Pembimbing:** Dr. Diah Puspito Wulandari, S.T., M.Sc. *(NIP. 19801219200501 2 001)*

</div>

> **Fokus Utama:** Manajemen Siklus Hidup Model AI Heterogen pada Satu GPU Edge (8 GB VRAM) Melalui Orkestrasi Microservices Adaptif.

---

<!-- 
SLIDE 2: DAFTAR ISI / AGENDA PRESENTASI
-->

# DAFTAR ISI PRESENTASI

## Roadmap Pembahasan

<div class="grid-2">

<div>

### **Bagian I: Fondasi Masalah**
- **01. Latar Belakang & Urgensi Masalah**
  - AI Heterogen pada Edge Kiosk
  - Bottleneck VRAM 8 GB & Ancaman OOM
- **02. Rumusan Masalah & Batasan Sistem**
  - 3 Research Questions Utama
  - Ruang Lingkup Hardware & Software

### **Bagian II: Metodologi & Arsitektur**
- **03. Metodologi I: Alur Penelitian & Arsitektur Sistem**
  - Tahapan Pelaksanaan Penelitian
  - Arsitektur Umum, UI/UX Kiosk & Orchestrator

</div>

<div>

### **Bagian III: Strategi & Evaluasi**
- **04. Metodologi II: Resource Management & 4 Strategi GPU**
  - Exclusive GPU Mode & Lifecycle State
  - Komparasi Strategi A, B, C, dan D
- **05. Metrik Evaluasi Kinerja Sistem**
  - Formula Matematis 5 Metrik Inti ($T_{\text{e2e}}$, $T_{\text{swap}}$, $T_{\text{infer}}$, $V_{\text{peak}}$, $SR$)
- **06. Status Progres & Rencana Selanjutnya**
  - Capaian Fase 1 & Roadmap Milestone M0–M4

### **Bagian IV: Penutup**
- **07. Kesimpulan Sementara & Tanya Jawab**

</div>

</div>

---

<!-- 
SLIDE 3: LATAR BELAKANG & PROBLEM STATEMENT
Fokus: Tunjukkan Urgensi, Masalah Riil, Keyword-Driven, Poin-Poin Padat
-->

# LATAR BELAKANG & PROBLEM STATEMENT

## Mengapa Orkestrasi pada Edge Kiosk Bersifat Sangat Urgent?

<div class="grid-2">

<div class="highlight-card">

### 🔴 **Kebutuhan vs Keterbatasan Fisik (The Real Problem)**

- **Beban Kerja Heterogen (Multimodal AI):**
  - Smart kiosk mengintegrasikan **Voice AI** (STT, LLM, TTS), **Vision AI** (VLM), serta fitur berat seperti **Virtual Try-on** dan **Photobooth**.
- **Ketergantungan Edge Computing (On-Premise):**
  - Eksekusi lokal 100% wajib dilakukan demi **privasi data visual/suara** dan **menghilangkan latensi koneksi cloud**.
- **Hambatan Fisik GPU Konsumen (8 GB VRAM):**
  - Mini PC kiosk (NVIDIA RTX 5060) memiliki batas memori keras **8.192 MB**. Total akumulasi bobot seluruh model melebihi **15+ GB**.

</div>

<div class="highlight-card">

### ⚠️ **Dampak Kritis Tanpa Orkestrasi Terkelola**

- **Ancaman Fatal OOM (Resource Contention):**
  - Menjalankan seluruh layanan bersamaan memicu `CUDA: Out of Memory` $\rightarrow$ kiosk crash dan sesi pengguna terputus.
- **Dilema Latensi Transisi (User Drop-Off):**
  - *Cold-reloading* model langsung dari SSD NVMe ke GPU memakan waktu **2–5+ detik**, merusak kepuasan interaksi sentuh/suara.
- **Kata Kunci Utama:**
  - `Edge AI`, `Microservices Orchestration`, `GPU Resource Contention`, `CUDA OOM Prevention`, `Low-Latency Transition`.

</div>

</div>

> **Urgensi Solusi:** Diperlukan *Application-Level Orchestrator* yang secara cerdas mengatur siklus hidup model (load/unload/prefetch) pada VRAM 8 GB tanpa mengorbankan responsivitas kios.

---

<!-- 
SLIDE 4: RUMUSAN MASALAH & TUJUAN PENELITIAN
Fokus: Poin-poin eksplisit, terukur, dan selaras dengan Bab 1
-->

# RUMUSAN MASALAH & TUJUAN PENELITIAN

## Menjawab Kebutuhan Operasional Smart Kiosk

<div class="grid-2">

<div class="highlight-card">

### 🎯 **Rumusan Masalah (Research Questions)**

1. **Arsitektur Orkestrasi:**
   - Bagaimana merancang sistem orkestrasi microservices lokal untuk mengintegrasikan layanan AI suara dan visual secara modular?
2. **Manajemen Sumber Daya GPU:**
   - Bagaimana mengelola siklus hidup model AI pada VRAM 8 GB agar terbebas dari ancaman *Out-of-Memory* (OOM)?
3. **Efisiensi Kinerja & Transisi:**
   - Bagaimana perbandingan efisiensi performa antara strategi alokasi memori (*All-Resident, Naive, Pinned Swap,* dan *Prefetch*) terhadap latensi pengguna?

</div>

<div class="highlight-card">

### 🚀 **Tujuan Penelitian (Research Objectives)**

1. **Membangun Sistem Orkestrasi:**
   - Mengembangkan *Application-Level Orchestrator* berbasis FastAPI (REST/WebSocket) yang mengontrol siklus hidup kontainer AI.
2. **Menerapkan Modul Resource Management:**
   - Mengimplementasikan mekanisme *Exclusive GPU Mode* dan *State-Machine Transition* yang adaptif terhadap kapasitas VRAM.
3. **Mengevaluasi Kinerja 5 Metrik Utama:**
   - Menguji dan membandingkan performa sistem secara kuantitatif berdasarkan total latensi, waktu swap, waktu inferensi, VRAM puncak, dan stabilitas sesi.

</div>

</div>

> **Ruang Lingkup:** Pengujian pada 1 unit perangkat Mini PC ASRock DeskMeet X600 (Linux Ubuntu 24.04 LTS, GPU RTX 5060 8 GB). Tidak mencakup modifikasi kernel driver GPU atau infrastruktur cloud multi-node.

---

<!-- 
SLIDE 5: METODOLOGI BAGIAN I — ALUR PENELITIAN & ARSITEKTUR SISTEM
Fokus: Diagram Alur Metodologi & 3 Arsitektur Sub-Sistem
-->

# METODOLOGI I: ALUR PENELITIAN & ARSITEKTUR SISTEM

## Alur Kerja Komprehensif dari Pengguna hingga Layanan AI

<div class="grid-2">

<div>

### 📊 **Tahapan Pelaksanaan Penelitian**

![Tahapan Penelitian](assets/diagrams/bab3_05_tahapan_pelaksanaan_penelitian.png)

- **8 Tahapan Terstruktur:**
  1. Analisis Kebutuhan $\rightarrow$ 2. Pemilihan Model $\rightarrow$ 3. Perancangan Arsitektur $\rightarrow$ 4. Implementasi Microservices $\rightarrow$ 5. Pengembangan Orkestrator $\rightarrow$ 6. Integrasi Fungsional $\rightarrow$ 7. Pengujian Kinerja $\rightarrow$ 8. Analisis Data.

</div>

<div>

### 🏗️ **3 Pilar Perancangan Arsitektur**

- **1. Arsitektur Umum (End-to-End):**
  - Menghubungkan *Touch/Audio Input* $\rightarrow$ UI Kiosk $\rightarrow$ Orchestrator $\rightarrow$ Microservices AI $\rightarrow$ Display.
  - ![Arsitektur Umum](assets/diagrams/bab3_01_arsitektur_umum.png)

- **2. UI/UX Chromium Kiosk (Layar Portrait 9:16):**
  - UI Web (HTML/JS/CSS) berjalan di Chromium Kiosk Mode dengan komunikasi WebSocket dua arah real-time.
  - ![Alur UI/UX](assets/diagrams/bab3_02_alur_pengguna_ui.png)

- **3. Orchestrator Engine (FastAPI Gateway):**
  - Mengelola *Service Registry*, *Session State*, *Request Dispatcher*, dan *Health Telemetry*.
  - ![Alur Orchestrator](assets/diagrams/bab3_03_alur_kerja_orchestrator.png)

</div>

</div>

---

<!-- 
SLIDE 6: METODOLOGI BAGIAN II — RESOURCE MANAGEMENT & 4 STRATEGI GPU
Fokus: Diagram Resource Management, Exclusive Mode, & Tabel Komparasi 4 Strategi
-->

# METODOLOGI II: RESOURCE MANAGEMENT & 4 STRATEGI GPU

## Solusi Alokasi VRAM 8 GB melalui Transisi Model Cerdas

<div class="grid-2">

<div>

### ⚙️ **Arsitektur Resource Management**

![Resource Management](assets/diagrams/bab3_04_alur_kerja_resource_management.png)

- **Exclusive GPU Mode:**
  - Saat layanan visual berat (*Try-on / Photobooth*) dipanggil, model suara di-*unload/suspend* sementara ke RAM sistem untuk memberikan **100% VRAM headroom**.
- **NVML Hardware Polling:**
  - Pemantauan alokasi VRAM real-time dengan frekuensi sampling tiap **50–100 ms**.

</div>

<div>

### 🔄 **Komparasi 4 Strategi Pengelolaan GPU**

| Strategi | Mekanisme Kerja | Kelebihan | Risiko / Kelemahan |
|---|---|---|---|
| **A. All-Resident** | Seluruh model tetap standby di VRAM | $T_{\text{swap}} = 0$ (Sangat cepat) | Rawan crash OOM saat model visual aktif |
| **B. Naive Swap** | Unload lama $\rightarrow$ Load baru dari SSD | Bebas OOM, memori bersih | Latensi swap tinggi (**2.0–5.0 s**) |
| **C. Pinned Memory** | Cache model di RAM Host (DDR5) via PCIe | Swap jauh lebih cepat (**< 1.0 s**) | Butuh alokasi RAM sistem yang cukup |
| **D. Prefetching** | Pemuatan awal saat user berinteraksi | Latensi terasa instan ($T_{\text{swap}} \approx 0$) | Prediksi harus presisi |

</div>

</div>

> **Inovasi Inti:** Menemukan *optimal operating point* antara penggunaan memori puncak ($V_{\text{peak}} \le 7.2\text{ GB}$) dan latensi responsif ($T_{\text{swap}} < 1.0\text{ s}$).

---

<!-- 
SLIDE 7: METRIK EVALUASI KINERJA SISTEM
Fokus: 5 Metrik Utama, Rumus Matematika, Cara Hitung, & Target PoC
-->

# METRIK EVALUASI KINERJA SISTEM

## 5 Tolok Ukur Kuantitatif Keberhasilan Orkestrasi

<div class="table-slide">

| No | Metrik Evaluasi | Formula Matematis | Metode & Alat Ukur | Target Kinerja PoC |
|:---:|---|---|---|:---:|
| **1** | **Total / Average Latency** | $T_{\text{e2e}} = T_{\text{response}} - T_{\text{request}}$ | Timestamp gateway (Event Request s.d. Response Audio/Visual pertama) | $\le 1.5\text{ s}$ (Suara)<br>$\le 3.5\text{ s}$ (Visual) |
| **2** | **Waktu Swap & Transisi** | $T_{\text{swap}} = t_{\text{ready}} - t_{\text{trigger}}$ | Selisih waktu kirim instruksi swap hingga endpoint `/ready` bernilai `true` | $< 1.0\text{ s}$ *(Strategi C/D)*<br>Baseline SSD: $< 4.0\text{ s}$ |
| **3** | **Inference Time** | $T_{\text{infer}} = t_{\text{complete}} - t_{\text{start}}$ | Profiling internal worker AI (waktu komputasi kernel murni tanpa I/O) | TTFT LLM $\le 800\text{ ms}$<br>Diffusion $\le 3000\text{ ms}$ |
| **4** | **Penggunaan VRAM Puncak** | $V_{\text{peak}} = \max_{t \in [t_0, t_1]} V(t)$ | Cuplikan NVML PyNVML / `nvidia-smi` kontinu tiap 50–100 ms | $\le 7.2\text{ GB}$ *(Headroom aman 10% dari 8 GB)* |
| **5** | **Tingkat Kestabilan Sesi** | $SR = \frac{N_{\text{sukses}}}{N_{\text{total}}} \times 100\%$ | Evaluasi total sesi pengujian tanpa crash `CUDA OOM` atau hang worker | $\ge 99.0\%$ *(Bebas fatal OOM pada 50+ sesi beruntun)* |

</div>

---

<!-- 
SLIDE 8: STATUS PROGRES SAAT INI & ROADMAP PENELITIAN
Fokus: Bukti pencapaian konkret dan langkah selanjutnya (Milestones M0-M4)
-->

# STATUS PROGRES & ROADMAP PENELITIAN

## Tracking Capaian Kerja dan Rencana Implementasi

<div class="grid-2">

<div class="highlight-card">

### ✅ **Progres yang Telah Diselesaikan (Fase 1)**

- **Arsitektur & Standar Dokumentasi:**
  - Telah memfinalisasi `METODOLOGI_PENELITIAN_BAB3.md`, `PERANCANGAN_SISTEM_BAB3.tex`, dan `METRICS_LATEX_BAB3.tex` lengkap dengan sitasi IEEE/Scopus.
- **Ekspor Diagram Vektor Resolusi Tinggi:**
  - 4 Diagram alir horizontal metodologi Bab 3 + 4 diagram alir strategi GPU telah dibuat di `assets/diagrams/`.
- **Spesifikasi & Audit Tech Stack:**
  - Penyelarasan spesifikasi hardware (Mini PC DeskMeet X600, RTX 5060 8GB) dan software stack (FastAPI, Chromium Kiosk, PyNVML, PyTorch).

</div>

<div class="highlight-card">

### 📅 **Roadmap Milestone Selanjutnya (M0 – M4)**

- **M0: Verifikasi Hardware & Standalone AI** *(Minggu Ini)*
  - Validasi PCIe throughput, batas aman VRAM 8 GB, dan isolasi model.
- **M1: Baseline Pipeline Suara Lokal**
  - Integrasi Faster-Whisper $\rightarrow$ Qwen LLM $\rightarrow$ Piper TTS (On-premise).
- **M2: Core Orchestrator & Benchmark 4 Strategi**
  - Implementasi State Machine & pengujian komparasi Strategi A, B, C, D.
- **M3: Integrasi Layanan Visual & Mode Eksklusif**
  - Integrasi Try-on dan Photobooth dengan swap memory aman.
- **M4: Integrasi Chromium Kiosk & Uji Stabilitas**
  - Pengujian end-to-end 50+ siklus interaksi kiosk potret 9:16.

</div>

</div>

---

<!-- 
SLIDE 9: PENUTUP & TANYA JAWAB
Gaya: Bersih, Profesional, Call to Action Akademik
-->

# TERIMA KASIH

### Sesi Tanya Jawab & Diskusi (Q&A)

<div class="highlight-card" style="text-align: center; padding: 25px;">

### **Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk**

**Rendy Lexxy Kurniawan — NRP 5024231007**  
Departemen Teknik Komputer, FTEIC — Institut Teknologi Sepuluh Nopember (ITS) Surabaya  

---

*"Mengoptimalkan Kinerja AI Heterogen Multimodal pada Edge Computing yang Efisien, Cepat, dan Bebas Kendala Memori."*

</div>

<div class="grid-2" style="margin-top: 15px; font-size: 0.9em;">

<div>

**Dosen Pembimbing:**
- Arta Kusuma Hernanda, S.T., M.T.
- Dr. Diah Puspito Wulandari, S.T., M.Sc.

</div>

<div>

**Kontak & Dokumentasi Proyek:**
- Repository: `proof-concept-smartkiosk`
- Dokumen Metodologi: `docs/METODOLOGI_PENELITIAN_BAB3.md`
- Diagram Teknis: `assets/diagrams/`

</div>

</div>
