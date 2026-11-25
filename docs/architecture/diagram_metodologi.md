# DOKUMENTASI 4 DIAGRAM ALIR & ARSITEKTUR METODOLOGI PENELITIAN (BAB III)

Dokumen ini memuat deskripsi akademik, fungsi, dan tautan gambar fisik `.png` untuk **4 Diagram Alir Metodologi Bab III** Tugas Akhir Rendy Lexxy Kurniawan. Seluruh diagram dirancang dengan **orientasi horizontal (kiri ke kanan / `LR`)**, menggunakan bahasa yang lugas, tidak berbelit-belit, dan telah diekspor otomatis dalam resolusi tinggi ke direktori `assets/diagrams/`.

---

## 1. Diagram 1: Arsitektur Umum & Relasi Antar-Tugas Besar

### a. Deskripsi & Fungsi
Diagram ini adalah gambaran makro (*high-level architecture*) yang menjelaskan bagaimana seluruh komponen sistem berinteraksi dari ujung ke ujung:
1. **Input Pengguna:** Sentuhan layar, audio suara, atau tangkapan kamera masuk ke lapisan Kiosk.
2. **UI/UX Chromium Kiosk (Tugas Besar 1):** Mengelola interaksi visual potret 9:16 dan mengirimkan permintaan aksi pengguna.
3. **Orchestrator (Tugas Besar 2):** Menjadi jembatan utama via API Gateway, melakukan routing, membaca konfigurasi registry, dan mengendalikan siklus hidup model (*lifecycle state machine*).
4. **Resource Management (Tugas Besar 3):** Menjalankan kebijakan alokasi memori GPU serta memantau kondisi VRAM/RAM secara real-time.
5. **Eksekusi Model AI & Output:** Memproses inferensi pada GPU fisik lokal RTX 5060, mengembalikan hasil visual/suara ke UI Kiosk, serta mencatat data ke berkas evaluasi.

### b. File Gambar Fisik
- **Path File:** [assets/diagrams/bab3_01_arsitektur_umum.png](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_01_arsitektur_umum.png)

![Diagram 1: Arsitektur Umum](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_01_arsitektur_umum.png)

---

## 2. Diagram 2: Alur Pengguna pada UI/UX Chromium Kiosk (Tugas Besar 1)

### a. Deskripsi & Fungsi
Diagram ini membedah perjalanan pengguna (*User Experience Flow*) dari awal mendekati mesin kiosk hingga mendapatkan hasil keluaran layanan AI:
1. Pengguna melihat **Halaman Utama / Standby Screen** pada layar potret 32 inci.
2. Pengguna memilih menu layanan (Percakapan Suara, Rekomendasi Busana, Virtual Try-On, atau AI Photobooth).
3. Halaman input aktif menerima aksi pengguna (audio, tangkapan webcam, atau sentuhan) dan mengirimkannya ke Gateway.
4. UI menampilkan indikator loading transisi saat orkestrator menyiapkan model.
5. Jika model siap, hasil interaksi disajikan (audio bicara, galeri foto, atau video langsung). Jika gagal, sistem menampilkan panduan mitigasi ramah pengguna sebelum kembali ke mode standby.

### b. File Gambar Fisik
- **Path File:** [assets/diagrams/bab3_02_alur_pengguna_ui.png](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_02_alur_pengguna_ui.png)

![Diagram 2: Alur Pengguna UI Kiosk](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_02_alur_pengguna_ui.png)

---

## 3. Diagram 3: Alur Kerja Orchestrator (Tugas Besar 2)

### a. Deskripsi & Fungsi
Diagram ini membedah logika internal orkestrator dalam memproses setiap permintaan dari UI Kiosk:
1. Permintaan masuk divalidasi oleh API Gateway dan dicocokkan dengan metadata layanan pada `services.yaml`.
2. Orkestrator memeriksa apakah model yang dibutuhkan sudah siap di GPU:
   - **Jika belum:** Orkestrator memicu instruksi *unload* pada model lama, menunggu konfirmasi pembebasan memori, lalu mengirim instruksi *load* model target.
   - **Pemeriksaan Kesiapan (*Readiness Check*):** Memastikan status HTTP 200 sebelum payload inferensi dialirkan.
3. Setelah berstatus `READY`, payload masukan diteruskan ke endpoint inferensi model.
4. Hasil komputasi diterima dan dikirimkan kembali ke UI Kiosk secara asinkronus.

### b. File Gambar Fisik
- **Path File:** [assets/diagrams/bab3_03_alur_kerja_orchestrator.png](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_03_alur_kerja_orchestrator.png)

![Diagram 3: Alur Kerja Orchestrator](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_03_alur_kerja_orchestrator.png)

---

## 4. Diagram 4: Alur Kerja Resource Management (Tugas Besar 3)

### a. Deskripsi & Fungsi
Diagram ini membedah mekanisme pemantauan sumber daya hardware dan pencatatan metrik evaluasi secara menyeluruh:
1. Menerima sinyal alokasi GPU dan mengidentifikasi strategi memori yang aktif.
2. Menjalankan prosedur alokasi dan swap memori (baik via Disk SSD, Host Pinned RAM, maupun Prefetching).
3. **Siklus Pemantauan:** *Background thread* NVML mencuplik alokasi VRAM secara kontinu setiap 50–100 ms untuk memverifikasi apakah batas aman ($V_{\text{peak}} \le 7,5\text{ GB}$) terpenuhi.
4. Merekam **Waktu Swap ($T_{\text{swap}}$)** dan **Waktu Inferensi ($T_{\text{infer}}$)**.
5. Menghitung **Latensi Total ($T_{\text{e2e}}$)** serta memeriksa **Kestabilan Sesi ($SR$)**.
6. Menyimpan kelima metrik tersebut ke dalam berkas log benchmark (CSV/JSONL) untuk bahan analisis kuantitatif Bab IV.

### b. File Gambar Fisik
- **Path File:** [assets/diagrams/bab3_04_alur_kerja_resource_management.png](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_04_alur_kerja_resource_management.png)

![Diagram 4: Alur Kerja Resource Management](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_04_alur_kerja_resource_management.png)
