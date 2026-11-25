# Ekstraksi Terstruktur & Analisis Dokumen Tugas Akhir Rendy Lexxy K (NRP 5024231007)

> **File Asli:** `docs/5024231007_Rendy Lexxy K_Draft_DIKUMPULIN.pdf` (27 Halaman)  
> **Status Dokumen:** Draf proposal awal (sebelum revisi PoC 30 Sept 2026).  
> **Tujuan Digest:** Menyajikan fakta naskah lama secara utuh, memetakan perbedaan kritis dengan PoC terbaru, dan menyimpan elemen visual untuk evaluasi perancangan.

---

## 1. Metadata Dokumen & Identitas Proposal
- **Judul Tertera:** *SISTEM ORKESTRASI LAYANAN AI BERBASIS MICROSERVICES PADA SISTEM SMART KIOSK*
- **Penulis:** Rendy Lexxy Kurniawan (NRP 5024231007)
- **Pembimbing:** Arta Kusuma Hernanda, S.T., M.T. (NIP 1996202311024)
- **Ko-Pembimbing:** Dr. Diah Puspito Wulandari, S.T., M.Sc. (NIP 19801219200501 2 001)
- **Afiliasi:** Program Studi S1 Teknik Komputer, Departemen Teknik Komputer, FTEIC - ITS Surabaya
- **Tahun Draft:** Tertera 2077 (catatan: salah ketik administratif, harus diperbaiki ke tahun berjalan).
- **Aset Gambar Asli:**  
  ![Logo ITS Halaman 1](images/5024231007_Rendy Lexxy K_Draft_DIKUMPULIN_p1_img1.png)

---

## 2. Rangkuman Isi Bab I (Pendahuluan) Versi Draft Lama

### 1.1 Latar Belakang
- Membahas transformasi digital pada smart kiosk mandiri yang berkembang dari mesin antrean/informasi sederhana menjadi sistem interaktif bertenaga kecerdasan buatan (*conversational agent*, *fashion recommendation*, *virtual try-on*, *photobooth*).
- Menekankan tantangan: penggabungan aneka model AI (Vision, Speech, Language) pada mesin komputasi edge lokal dengan sumber daya memori terbatas menimbulkan perebutan sumber daya (*resource contention*) dan *out-of-memory* (OOM).
- Menawarkan arsitektur microservices untuk memisahkan beban kerja ke dalam modul independen yang berkomunikasi melalui API terstruktur.

### 1.2 Rumusan Masalah dalam Naskah Lama
1. Bagaimana merancang dan membangun arsitektur microservices untuk orkestrasi layanan AI pada perangkat smart kiosk edge?
2. Bagaimana mekanisme penjadwalan (*scheduling*) dan alokasi sumber daya memori GPU agar perpindahan antar layanan AI berjalan mulus tanpa terjadi OOM?
3. Bagaimana pengaruh strategi orkestrasi terhadap latensi respons inferensi, throughput, dan pemanfaatan memori GPU?

### 1.3 Batasan Masalah dalam Naskah Lama
1. Sistem diimplementasikan pada 1 perangkat fisik edge lokal (Mini PC) dengan spesifikasi NVIDIA GPU RTX 5060 8 GB VRAM.
2. Tidak melatih model AI baru; fokus pada integrasi layanan yang sudah ada.
3. Layanan AI mencakup: Conversational AI (STT/LLM/TTS), Fashion Recommendation, Virtual Try-on, dan Photobooth.
4. Antarmuka kiosk dikembangkan untuk layar sentuh berorientasi potret (9:16).

---

## 3. Rangkuman Bab II (Tinjauan Pustaka) Versi Draft Lama

- **Penelitian Terdahulu:** Mengutip implementasi edge AI terdahulu seperti MiniDeep (Chen et al., 2022) dan studi arsitektur microservices edge computing.
- **Landasan Teori yang Dibahas:**
  - Konsep Smart Kiosk dan Edge Computing.
  - Arsitektur Microservices dan Containerization (Docker).
  - Model Inferensi Deep Learning (LLM, Diffusion Model, VLM).
  - Manajemen Memori GPU NVIDIA (VRAM, CUDA Context, Driver Runtime).

---

## 4. Rangkuman Bab III (Metodologi Penelitian) Versi Draft Lama & Peta Perbedaan dengan PoC Terbaru

Terdapat evolusi arsitektur penting antara draf ini dengan `PROOF_OF_CONCEPT.md` (PoC revisi A, 30 September 2026):

| Komponen / Aspek | Draft PDF Lama (`5024231007_...`) | Keputusan Final PoC (`PROOF_OF_CONCEPT.md` & `DECISIONS.md`) | Catatan Revisi Skripsi |
|---|---|---|---|
| **Frontend UI Kiosk** | Flutter Desktop (Linux) | **Web Application (HTML/CSS/JS) via Chromium Kiosk Mode** | Diperbarui sesuai ADR-001 (lebih fleksibel, streaming WebRTC/video lebih stabil). |
| **Batas Orkestrator** | Sering menyebut "penjadwalan GPU" yang berisiko disalahartikan sebagai kernel scheduling | **Application-Level Lifecycle & Resource-Aware Orchestrator** | Diperjelas sesuai ADR-002: kontribusi bukan driver kernel, melainkan manajemen status model. |
| **Strategi Lifecycle** | Skenario A (aktif bersamaan) vs Skenario B (bergantian) | **4 Strategi Terkontrol:** (a) All-Resident, (b) Naive Load/Unload, (c) Pinned Swap, (d) Prefetch | Menggunakan taksonomi 4 strategi dengan diagram alur terstandarisasi. |
| **Metrik Evaluasi** | Latensi umum, CPU/GPU util | **Taksonomi Formal 10 Metrik (MTR-01 s.d MTR-10)** di `docs/METRICS.md` | Memisahkan Load-to-Ready Time, Unload Time, dan Inference Latency. |
