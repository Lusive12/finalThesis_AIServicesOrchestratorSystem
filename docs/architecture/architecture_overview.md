# Penjelasan Diagram Arsitektur Umum Sistem Smart Kiosk

> **Referensi Diagram:** [bab3_01_arsitektur_umum.png](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/assets/diagrams/bab3_01_arsitektur_umum.png)  
> **Naskah Terkait:** [PERANCANGAN_SISTEM_BAB3.tex](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/PERANCANGAN_SISTEM_BAB3.tex) & [DIAGRAM_METODOLOGI_BAB3.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/DIAGRAM_METODOLOGI_BAB3.md)

---

## DAFTAR ISI
1. [Versi A: Penjelasan Formal Akademik (Untuk Laporan Skripsi Bab III)](#versi-a-penjelasan-formal-akademik)
2. [Versi B: Penjelasan Mudah (Analogi Restoran Cepat Saji)](#versi-b-penjelasan-mudah)

---

<a name="versi-a-penjelasan-formal-akademik"></a>
## Versi A: Penjelasan Formal Akademik (Gaya Skripsi / Sidang)

Diagram arsitektur umum sistem kios cerdas menggambarkan interaksi hierarkis dan pertukaran data dari ujung ke ujung (*end-to-end*), mulai dari lapisan interaksi fisik pengguna, antarmuka pengguna, pengatur layanan (*orchestrator*), pengelola sumber daya perangkat keras (*resource management*), hingga eksekusi inferensi model kecerdasan artifisial pada unit akselerator grafis lokal.

### 1. Alur Permintaan Pengguna (User Interaction Flow)
1. **Modul 1: Input Pengguna (User Input Layer)**  
   Titik awal interaksi fisik pengguna dengan kios cerdas. Menangkap tiga modalitas masukan:
   - Sentuhan jari pada panel layar sentuh potret 32 inci.
   - Sinyal gelombang suara ucapan pengguna melalui mikrofon USB *far-field array*.
   - Aliran visual (*video frame*) wajah dan postur tubuh melalui kamera web USB 1080p.
2. **Modul 2: UI/UX Chromium Kiosk (Tugas Besar 1)**  
   Aplikasi antarmuka web potret (rasio 9:16, resolusi $1080 \times 1920$) yang dieksekusi melalui peramban Chromium dalam mode kios layar penuh (*fullscreen kiosk mode*). Modul ini bertugas:
   - Menampilkan menu layanan interaktif dan status sistem secara visual.
   - Mengemas masukan pengguna menjadi muatan permintaan (*request payload*).
   - Menjalin komunikasi dupleks dengan Orchestrator melalui protokol HTTP REST API (perintah diskrit) dan WebSocket (pembaruan status asinkronus).
3. **Modul 3: AI Service Orchestrator (Tugas Besar 2)**  
   Pusat kendali logika aplikasi kios cerdas berbasis Python dan FastAPI. Modul ini menjalankan:
   - **API Gateway:** Memvalidasi, mengautentikasi, dan merutekan setiap permintaan aksi pengguna.
   - **Service Registry (`services.yaml`):** Memetakan endpoint, kebutuhan estimasi VRAM, serta karakteristik eksklusivitas masing-masing layanan AI.
   - **Lifecycle State Machine:** Mengendalikan status siklus hidup model (`STOPPED`, `STARTING`, `READY`, `STOPPING`, `ERROR`).
   - Mencegah tabrakan pemanggilan layanan secara konkuren (*concurrency locking*).

### 2. Alur Pengelolaan Sumber Daya & Eksekusi Model (Resource & Execution Flow)
4. **Modul 4: Resource Management (Tugas Besar 3)**  
   Pengendali alokasi memori fisik GPU dan penjamin stabilitas sistem komputasi edge. Modul ini bertanggung jawab:
   - Mengatur pembebanan model berdasarkan 4 strategi evaluasi: *(a) All-Resident*, *(b) Naive Load/Unload*, *(c) Pinned-Memory Swap*, dan *(d) Prefetch*.
   - Menerapkan mekanisme penghalang (*barrier state transition*) untuk layanan visual bermemori besar (*Exclusive GPU Mode*).
   - Mengambil sampel metrik memori VRAM fisik ($V_{\text{peak}}$) dan utilisasi komputasi secara kontinu setiap 50–100 ms menggunakan pustaka resmi PyNVML (*Python NVIDIA Management Library*).
5. **Modul 5: Eksekusi Model AI Lokal (Local AI Engine)**  
   Klaster proses/kontainer model kecerdasan artifisial siap pakai (*open-weight models*) yang berjalan secara lokal pada mini PC kios:
   - Pipeline Percakapan Suara: STT (Faster-Whisper), LLM Lokal (Qwen/Llama via llama.cpp/Ollama), dan TTS (Piper).
   - Layanan Rekomendasi Busana: Vision-Language Model & Generative Model.
   - Layanan Mode Eksklusif: Video Virtual Try-On dan AI Photobooth.
   Seluruh komputasi paralel dieksekusi secara akseleratif pada GPU fisik lokal **NVIDIA GeForce RTX 5060 (8 GB VRAM)** melalui bus PCIe.
6. **Modul 6: Keluaran Sistem & Pencatatan Evaluasi (System Output & Evaluation Logging)**  
   Hasil komputasi inferensi didistribusikan ke dua jalur:
   - **Jalur Pengguna:** Mengembalikan respons sintesis audio ke speaker, animasi wajah ke layar, atau galeri citra/video hasil olahan ke UI Chromium Kiosk.
   - **Jalur Evaluasi Ilmiah:** Menyimpan rekaman 5 metrik evaluasi kinerja ke dalam berkas log terstruktur (`results/*.csv` dan `results/*.jsonl`) sebagai bahan empiris analisis Bab IV skripsi.

---

<a name="versi-b-penjelasan-mudah"></a>
## Versi B: Penjelasan Mudah (Analogi Restoran Cepat Saji Modern)

Agar arsitektur ini sangat mudah dipahami oleh siapa saja, bayangkan sistem Smart Kiosk ini seperti sebuah **Restoran Cepat Saji Pintar**:

```text
[Pelanggan]              ---> Datang ke kasir layar sentuh untuk memesan menu.
[Layar Kiosk (UI/UX)]    ---> Layar pemesanan tempat pelanggan memilih makanan/minuman.
[Manajer Restoran]       ---> Orchestrator yang mengatur antrean dan pesanan.
[Kepala Dapur]           ---> Resource Management yang mengatur kompor dan meja masak (GPU).
[Koki Spesialis (AI)]    ---> Model-model AI (Koki Pembuat Burger, Koki Minuman, Koki Steak).
[Meja Masak Terbatas]    ---> GPU RTX 5060 (VRAM 8 GB) yang tempatnya terbatas!
```

### Cerita Alur Kerjanya:

1. **Pelanggan Datang (Input Pengguna):**  
   Pengguna menyentuh layar, berbicara ke mikrofon, atau berdiri di depan kamera kios.
2. **Layar Kios Menerima Pesanan (UI/UX Chromium Kiosk):**  
   Layar menampilkan tombol-tombol pilihan menu. Saat disentuh, layar langsung melapor ke Manajer Restoran: *"Bos, pelanggan ingin mencoba fitur Virtual Try-On pakaian!"*
3. **Manajer Restoran Memeriksa Aturan (Orchestrator):**  
   Manajer melihat buku menu (`services.yaml`). Manajer tahu bahwa *Virtual Try-On* adalah pesanan besar yang butuh tempat luas di dapur. Manajer tidak langsung memasak, melainkan berkoordinasi dengan Kepala Dapur.
4. **Kepala Dapur Menyiapkan Meja Masak (Resource Management & VRAM):**  
   Kepala Dapur melihat meja masak (VRAM 8 GB). *"Meja masak saat ini sedang dipakai koki percakapan suara. Karena Virtual Try-On butuh meja yang sangat luas, koki percakapan harus beres-beres dan keluar dari meja masak terlebih dahulu!"*  
   Setelah meja masak bersih (VRAM kosong), Kepala Dapur memberi lampu hijau: *"Meja sudah siap!"*
5. **Koki Mulai Memasak (Eksekusi Model AI di GPU):**  
   Model Virtual Try-On masuk ke GPU RTX 5060 dan memproses pakaian virtual pada video pengguna dalam hitungan detik.
6. **Pesanan Disajikan & Catatan Dibuat (Output & Logging):**  
   - Pengguna melihat pantulan dirinya memakai pakaian baru di layar kios secara mulus.
   - Di saat yang sama, manajer mencatat di buku kasir: berapa lama waktu memasak tadi, dan berapa banyak ruang meja yang terpakai, agar pemilik restoran tahu restorannya berjalan sangat efisien tanpa pernah meledak (*out of memory*)!
