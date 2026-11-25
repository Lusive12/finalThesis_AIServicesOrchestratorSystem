# guardrail.md — Batasan Ruang Lingkup & Panduan Agent AI

> **Lokasi:** `docs/guardrail.md`  
> **Fungsi:** Menetapkan batas tegas apa yang boleh dan tidak boleh dilakukan oleh Agent AI saat memodifikasi kode, konfigurasi, maupun dokumen naskah skripsi.  
> **Kapan AI membaca:** Wajib dipatuhi pada setiap sesi interaksi pengembangan proyek.

---

## 1. Identitas & Batasan Judul Tugas Akhir

- **Judul Resmi:** *“Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk”*.
- **Aturan Ketat:** DILARANG menambahkan atau mengganti kata judul menjadi *"Rancang Bangun..."*, *"Implementasi..."*, atau sejenisnya tanpa persetujuan eksplisit pemilik TA dan dosen pembimbing.

---

## 2. Batas Kontribusi Teknis (Scope of Work)

### 2.1 Yang Menjadi Kontribusi Proyek (In-Scope)
1. **API Gateway & Routing:** FastAPI REST & WebSocket untuk menghubungkan UI Kiosk dan microservices AI.
2. **AI Service Orchestrator:** Service registry (`configs/services.yaml`), Lifecycle State Machine (`STOPPED`, `STARTING`, `READY`, `STOPPING`, `ERROR`), dan mode manager.
3. **Resource Management:** Evaluasi komparatif 4 strategi pengelolaan memori GPU (*All-Resident, Naive, Pinned Swap, Prefetch*), penanganan barrier mode eksklusif, dan sampling NVML kontinu.
4. **Kiosk UI:** Antarmuka web potret 9:16 di Chromium Kiosk Mode.
5. **Evaluasi Kuantitatif:** Pengukuran empiris 5 metrik inti ($T_{\text{e2e}}$, $T_{\text{swap}}$, $T_{\text{infer}}$, $V_{\text{peak}}$, $SR$).

### 2.2 Yang BUKAN Kontribusi Proyek (Strictly Out-of-Scope)
- **Pelatihan Model AI dari Nol (*Model Training from Scratch*):** Proyek ini memanfaatkan model *open-weight* siap pakai; fokus ada pada level orkestrasi sistem.
- **Kernel-level GPU Scheduling / Driver Modification:** Pengelolaan sumber daya dilakukan pada tingkat aplikasi/proses/kontainer, bukan modifikasi driver NVIDIA atau GPU virtualization (vGPU/MIG).
- **Infrastruktur Multi-Node / Cloud-First:** Target sistem adalah *standalone on-premise edge computing* pada satu Mini PC fisik dengan 1 GPU fisik lokal (NVIDIA RTX 5060 8 GB VRAM).

---

## 3. Larangan Keras bagi AI Agent (Strict Guardrails)

1. **Dilarang Halusinasi Data & Angka Benchmark:**
   - Dilarang mengarang angka latensi, konsumsi VRAM, throughput, atau persentase kestabilan.
   - Bedakan secara tegas antara **Target PoC** (misal: 100 giliran percakapan, VRAM $\le 7,5\text{ GB}$) dengan **Hasil Terukur Aktual**.
2. **Dilarang Mengarang Sitasi & Referensi Ilmiah:**
   - Dilarang membuat-buat judul paper fiktif, nama penulis, DOI, atau nama konferensi/jurnal. Semua referensi harus nyata dan tercatat di `docs/bab3_latex/references.bib`.
3. **Dilarang Mengubah Stack Utama Tanpa Persetujuan:**
   - Stack resmi UI adalah **Web App (HTML/CSS/JS) pada Chromium Kiosk Fullscreen**. Dilarang mengubahnya menjadi Flutter Desktop atau teknologi lain.
4. **Dilarang Perintah Terminal Destruktif:**
   - Dilarang menjalankan perintah pembersihan luas seperti `pkill -f python` atau `killall` yang berisiko mematikan proses pengguna lain pada PC lab bersama. Selalu periksa PID terlebih dahulu.
5. **Integritas Catatan Kegagalan:**
   - Dilarang menghapus riwayat run eksperimen yang gagal atau mengalami OOM. Semua insiden kegagalan wajib dicatat sebagai data ilmiah analisis Bab IV.
