# Peta Jalan Tugas Akhir dan Revisi Bab I–III
**Judul:** Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk  
**Basis:** `PROOF_OF_CONCEPT.md`, revisi A, 30 September 2026.  
**Status:** draf kerja; sesuaikan dengan implementasi aktual dan arahan pembimbing.

> Berkas Bab I–III versi lama tidak dilampirkan. Karena itu, dokumen ini merupakan draf revisi terintegrasi berdasarkan PoC dan keputusan proyek yang sudah diketahui, bukan penyuntingan baris demi baris atas naskah lama.

# 1. Ringkasan proyek dan batas kontribusi

Fokus TA ini adalah **gateway, orkestrator, UI kiosk, dan pengelolaan lifecycle model pada GPU lokal**. Sistem mengintegrasikan layanan AI milik enam tugas akhir pada satu mini PC dengan GPU RTX 5060 8 GB VRAM. Kontribusi bukan melatih model AI baru atau membangun scheduler GPU tingkat kernel/cluster. Kontribusinya adalah mengimplementasikan layanan modular dengan kontrak API seragam, mengelola pemuatan/pelepasan model, mengatur perpindahan mode, memantau penggunaan sumber daya, dan mengevaluasi trade-off antara penggunaan memori dan latensi.

## 1.1 Platform dan perangkat

| Komponen | Informasi PoC | Tindakan verifikasi |
|---|---|---|
| Mini PC | ASRock DeskMeet | Verifikasi model motherboard |
| CPU/RAM/SSD | AMD Ryzen 5, RAM 16 GB, SSD 1 TB | Catat model CPU, tipe/slot RAM, kapasitas kosong SSD |
| GPU | Gigabyte NVIDIA RTX 5060 Low Profile, VRAM 8 GB | Verifikasi GPU, VRAM, driver, dan akses runtime |
| OS | Ubuntu Desktop GNOME | Catat versi Ubuntu/kernel |
| Remote access | Tailscale | Gunakan untuk administrasi jika PC diakses dari laptop |
| Layar | Layar sentuh potret, estimasi 32 inci 1080 × 1920 | Verifikasi resolusi, HDMI, USB sentuh ke Ubuntu |
| Periferal | Kamera USB 1080p/30 fps, mic USB, speaker; LED opsional | Uji masing-masing pada tahap awal |

Angka dan kebutuhan model dalam PoC masih berupa estimasi sampai diukur. Jangan menulis model motherboard, versi CUDA/driver, konsumsi VRAM, atau target latensi sebagai hasil yang telah terbukti sebelum verifikasi.

## 1.2 Pembagian tanggung jawab

| Pemilik TA | Layanan | Kebutuhan orkestrator |
|---|---|---|
| Rendy | Gateway, orkestrator, UI kiosk | Registry, lifecycle model, manajemen mode, GPU, metrik, integrasi |
| Ferdie | STT, LLM, TTS | Mengatur pipeline percakapan dan model per giliran bicara |
| Gung | Avatar real-time | Avatar mungkin harus berjalan bersamaan dengan TTS |
| Ria | Rekomendasi busana: VLM lalu generasi gambar | Dua tahap per permintaan; VLM dan difusi mungkin harus bergantian |
| Erdi | Virtual try-on video | Mode eksklusif yang menggunakan GPU selama sesi |
| Deva | AI photobooth | Mode eksklusif; model lain dilepas sesuai kebijakan |

Enam fitur tidak berarti hanya enam proses model. Pipeline suara terdiri atas beberapa model, rekomendasi busana menggunakan VLM dan model generasi gambar, dan layanan avatar dapat berjalan bersamaan dengan TTS. Registry harus membedakan **fitur kiosk, layanan API, dan setiap proses/model yang menggunakan VRAM**.

## 1.3 Stack yang selaras dengan PoC

PoC mengusulkan UI web potret di Chromium mode kiosk, FastAPI/REST/WebSocket sebagai gateway, Python sebagai orkestrator, NVML untuk pemantauan GPU, dan layanan model dalam proses atau container terpisah. Maka stack awal yang paling konsisten adalah:
- UI web potret pada Chromium kiosk;
- Python + FastAPI untuk gateway;
- Python untuk orchestrator dan benchmark;
- REST API untuk request-response, WebSocket untuk streaming jika dibutuhkan;
- NVML (binding Python) dan `nvidia-smi` untuk metrik GPU;
- Docker/Compose atau proses terpisah sesuai kebutuhan runtime;
- runtime model dipilih dan dipin versinya setelah lolos pengujian lokal.

Flutter Desktop sempat dipertimbangkan sebelumnya, tetapi bukan UI yang tercantum dalam PoC saat ini. Gunakan Flutter hanya jika tim menyetujui perubahan rancangan dan seluruh integrasi disesuaikan.

# 2. Roadmap dan milestone

## M0 — Verifikasi lingkungan dan kelayakan model (PoC-0)
**Pekerjaan:** verifikasi motherboard, RAM, PCIe, GPU, VRAM, OS, driver, layar sentuh, kamera, mic, speaker, suhu, dan daya. Jalankan setiap kandidat model sendiri-sendiri; ukur VRAM puncak, waktu load, latensi inferensi, kebutuhan RAM, dan versi dependensi. Uji try-on video paling awal karena risikonya tinggi pada VRAM 8 GB.

**Keluaran:** inventaris perangkat, daftar versi software, matriks kompatibilitas model, baseline tiap model, daftar risiko.

**Lulus jika:** kandidat yang dipilih berjalan sendiri pada GPU; VRAM puncak dan waktu load tercatat; periferal terdeteksi. Jika gagal, ganti kandidat atau dokumentasikan batasannya sebelum lanjut.

## M1 — Baseline pipeline suara (PoC-1)
Bersama Ferdie, buktikan STT → LLM → TTS berjalan lokal tanpa API cloud. Rendy mencatat timestamp akhir ucapan, teks STT final, token pertama LLM, dan audio pertama bila tersedia. Pisahkan latensi per tahap dan latensi ujung ke ujung. Gunakan rekaman ID/EN yang sama untuk pengujian berulang.

**Keluaran:** pipeline suara dasar, log, baseline latensi. Evaluasi kualitas STT/LLM/TTS merupakan tanggung jawab pemilik layanan, kecuali ada kesepakatan tambahan.

## M2 — Orkestrator minimum dan kontrak layanan (PoC-2)
Definisikan registry: ID model, endpoint/port, kebutuhan VRAM, mode, sifat eksklusif, dependensi, dan metode load/unload. Implementasikan endpoint `GET /health`, `POST /load`, `POST /unload`, `POST /infer` atau WebSocket, dan `GET /metrics`. Buat benchmark otomatis dan log terstruktur. Implementasikan strategi pengelolaan model yang memang didukung runtime.

**Keluaran:** orchestrator, registry, kontrak API, skrip benchmark, data mentah dan tabel perbandingan.

**Target PoC:** 100 giliran percakapan berturut-turut tanpa OOM, VRAM puncak ≤ 7,5 GB, dan tabel perbandingan empat strategi tersedia. Ini adalah target penerimaan, bukan hasil yang boleh diklaim sebelum diuji.

## M3 — Integrasi layanan visual dan mode eksklusif (PoC-3)
Integrasikan layanan Ria, Erdi, Deva, dan Gung melalui kontrak yang sama. Sepakati anggaran VRAM avatar dengan Ferdie/Gung. Uji transisi percakapan → rekomendasi busana → try-on → photobooth → percakapan. Try-on perlu memiliki jalur keluar yang tidak bergantung pada model GPU yang sedang tidak tersedia, misalnya timer atau pengenal CPU sesuai kesepakatan.

**Keluaran:** matriks mode, uji transisi, dan bukti perpindahan tanpa restart aplikasi.

## M4 — UI kiosk dan stabilitas (PoC-4)
Bangun UI potret untuk mode percakapan, galeri gambar, video langsung, dan photobooth. Tambahkan status loading, progres, error, dan pemulihan. Konfigurasikan Chromium kiosk/autostart. Jalankan demo end-to-end dan uji kestabilan 8 jam.

**Keluaran:** prototipe terintegrasi, laporan uji kestabilan, dokumentasi operasi.

**Target PoC:** demo penuh dapat dijalankan pengguna baru dan kiosk bertahan 8 jam tanpa kebocoran VRAM yang menyebabkan kegagalan. Definisikan kebocoran/degradasi secara operasional.

## Urutan kerja praktis

1. Minggu awal: verifikasi perangkat dan jalankan satu model lokal.
2. Berikutnya: kumpulkan metadata tiap layanan dari pemilik TA dan sepakati kontrak API.
3. Buat registry dan log; implementasikan `health`, `load`, `unload`, dan readiness timeout.
4. Buat benchmark sebelum UI selesai; ukur penggunaan VRAM sebelum/saat/setelah unload.
5. Implementasikan strategi A–D hanya sejauh didukung runtime.
6. Integrasikan layanan visual dan kebijakan mode.
7. Integrasikan UI, autostart, dan uji kestabilan.

UI dapat dikembangkan paralel setelah kontrak disepakati. Jangan menunggu seluruh UI selesai untuk mulai menguji orkestrator.

# 3. Strategi eksperimen dan metrik

| Strategi | Perilaku | Hal yang perlu dicatat |
|---|---|---|
| A. All-resident | Model yang dipilih tetap di VRAM | Latensi rendah saat model siap, tetapi memori tinggi; mungkin perlu model lebih kecil |
| B. Naive load/unload | Muat saat dibutuhkan, lepaskan setelah selesai | Biaya load/swap; pisahkan cache dingin dan hangat |
| C. Pinned-memory swap | Bobot di pinned RAM, dipindahkan ke VRAM saat diperlukan | Hanya sah bila runtime benar-benar mendukung; RAM bisa menjadi bottleneck |
| D. Prefetch | Model berikutnya dimuat sebelum dibutuhkan | Latensi dapat turun, tetapi memerlukan RAM/VRAM dan prediksi urutan |

**Masalah validitas penting:** strategi A yang menggunakan model kecil tidak dapat dibandingkan secara langsung dengan strategi lain yang menggunakan model berbeda seolah-olah hanya strategi yang berubah. Buat dua analisis terpisah bila perlu: (1) perbandingan strategi dengan model/workload identik pada subset yang muat; (2) perbandingan profil sistem yang menggunakan konfigurasi model berbeda.

PoC mencatat bahwa pinned-memory swap tidak tersedia di semua runtime; llama.cpp/Ollama tidak otomatis menyediakan mekanisme yang dimaksud. Putuskan runtime sebelum menyatakan strategi C telah diimplementasikan. Jika tidak ada runtime yang mendukung, nyatakan keterbatasan dan jangan membuat klaim palsu.

| Metrik | Definisi/cara ukur |
|---|---|
| VRAM puncak | Maksimum deret sampel NVML selama pengujian; PoC mengusulkan sampling 50–100 ms |
| Waktu load | Dari permintaan load sampai model siap menerima inferensi |
| Waktu unload | Dari permintaan unload sampai proses berhenti dan penggunaan VRAM sesuai definisi uji |
| Waktu perpindahan/swap | Dari awal transisi sampai layanan tujuan siap |
| Latensi inferensi | Dari request inferensi sampai respons selesai; streaming juga ukur first token/audio |
| Latensi percakapan | Akhir ucapan pengguna sampai audio pertama |
| Keberhasilan | Request berhasil dibagi total request |
| Stabilitas | OOM, crash, error, timeout, dan pemulihan setelah transisi |
| Metrik visual | FPS dan latensi kamera-ke-layar untuk try-on bila instrumentasi tersedia |

Gunakan input audio/gambar yang sama, parameter yang sama, kondisi awal terdokumentasi, warm-up terpisah, dan mulai dengan 10 pengulangan per kondisi. Jalankan 100 giliran percakapan untuk target PoC. Simpan data mentah, jangan buang OOM atau timeout, dan laporkan median/rata-rata/rentang serta p95 bila jumlah sampel memadai.

# 4. Draf revisi Bab I — Pendahuluan

## 1.1 Latar Belakang

Smart kiosk merupakan sistem interaktif yang dapat mengintegrasikan antarmuka pengguna dengan berbagai layanan digital untuk mendukung penyampaian informasi dan pelaksanaan fungsi secara mandiri. Perkembangan kecerdasan buatan memungkinkan kiosk menyediakan interaksi yang lebih beragam, seperti percakapan berbasis suara, analisis citra, rekomendasi busana, virtual try-on, dan pembuatan foto berbasis AI. Penggabungan beberapa layanan tersebut meningkatkan kebutuhan komputasi karena setiap layanan dapat menggunakan model, dependensi, dan sumber daya yang berbeda. Oleh karena itu, smart kiosk yang mengintegrasikan beberapa layanan AI memerlukan mekanisme pengelolaan layanan yang terstruktur.

Arsitektur microservices dapat digunakan untuk memisahkan layanan AI menjadi komponen yang berkomunikasi melalui antarmuka yang ditentukan. Pemisahan tersebut memungkinkan layanan dikembangkan dan diperbarui secara mandiri serta membantu membatasi dampak kegagalan suatu layanan terhadap komponen lain. Namun, pemisahan layanan tidak dengan sendirinya menyelesaikan persoalan penggunaan sumber daya, karena beberapa proses AI tetap dapat menggunakan GPU dan memori GPU yang sama. Pengelolaan layanan perlu mempertimbangkan kebutuhan memori dan pola penggunaan setiap model.

Platform dalam penelitian ini dirancang untuk berjalan pada satu mini PC dengan GPU NVIDIA RTX 5060 berkapasitas VRAM 8 GB. Platform mengintegrasikan pipeline percakapan multibahasa, avatar digital, rekomendasi busana, virtual try-on video, dan AI photobooth. Layanan tersebut memiliki pola penggunaan GPU yang berbeda: sebagian memproses model secara berurutan, sebagian memerlukan proses bersamaan, dan sebagian lain membutuhkan GPU secara eksklusif selama sesi. Kondisi ini menimbulkan tantangan untuk menentukan model yang perlu dimuat, waktu pelepasan model, serta perpindahan layanan tanpa mengganggu keseluruhan kiosk.

Kapasitas VRAM yang terbatas membuat seluruh model tidak selalu dapat dipertahankan di GPU secara bersamaan. Sebaliknya, memuat model hanya ketika dibutuhkan dapat meningkatkan waktu tunggu karena model perlu disiapkan sebelum inferensi. Beberapa strategi yang dapat dievaluasi meliputi mempertahankan model di VRAM, melakukan load/unload ketika diperlukan, memindahkan bobot melalui RAM apabila runtime mendukungnya, dan memuat awal model berikutnya. Setiap strategi memiliki trade-off terhadap penggunaan memori, latensi, dan kestabilan yang perlu diuji pada perangkat aktual.

Berdasarkan permasalahan tersebut, penelitian ini berfokus pada pengembangan sistem orkestrasi layanan AI berbasis microservices untuk smart kiosk. Sistem mencakup gateway, registry, pengelolaan lifecycle model, kebijakan perpindahan mode, antarmuka kiosk, serta pencatatan metrik kinerja. Pengujian membandingkan strategi pengelolaan model dengan workload terkontrol, menggunakan metrik penggunaan VRAM/RAM, waktu pemuatan dan perpindahan, latensi, keberhasilan permintaan, serta kejadian kegagalan. Hasilnya digunakan untuk mengevaluasi trade-off dan batas penerapan strategi pada satu perangkat kiosk dengan sumber daya terbatas.

## 1.2 Rumusan Masalah

1. Bagaimana merancang dan mengimplementasikan orkestrasi berbasis microservices yang mengintegrasikan layanan AI pada satu smart kiosk?
2. Bagaimana menerapkan kontrak layanan dan pengelolaan lifecycle model untuk mengatur penggunaan GPU bersama pada perangkat dengan VRAM 8 GB?
3. Bagaimana perbandingan strategi all-resident, naive load/unload, pinned-memory swap, dan prefetch berdasarkan penggunaan VRAM, waktu pemuatan/perpindahan, latensi, dan keberhasilan layanan?
4. Sejauh mana sistem mendukung perpindahan antarmode dan kestabilan tanpa perlu restart aplikasi kiosk?

## 1.3 Batasan Masalah

1. Pengujian dibatasi pada satu mini PC Linux/Ubuntu dengan satu GPU RTX 5060 8 GB sesuai inventaris PoC; spesifikasi aktual diverifikasi sebelum eksperimen.
2. Kontribusi berfokus pada gateway, UI kiosk, registry, orkestrator, lifecycle model, pemantauan sumber daya, dan integrasi layanan.
3. Model berasal dari implementasi yang tersedia dan berjalan lokal; penelitian tidak melatih model AI dari awal dan tidak menggunakan cloud API sebagai jalur inferensi utama.
4. Layanan mencakup domain percakapan (STT, LLM, TTS), avatar, rekomendasi busana, try-on video, dan photobooth, sesuai kelayakan hasil uji awal.
5. Pengelolaan GPU dibatasi pada tingkat aplikasi/proses/model; tidak membangun scheduler GPU tingkat kernel, GPU virtualization, atau scheduler cluster.
6. Strategi pinned-memory hanya diuji jika runtime mendukungnya secara nyata. Strategi yang tidak dapat diimplementasikan dicatat sebagai keterbatasan, bukan dianggap berhasil.
7. Metrik utama mencakup VRAM/RAM, load/unload/swap, latensi, keberhasilan, OOM/error/timeout, dan kestabilan. Metrik kualitas model khusus tetap menjadi tanggung jawab pemilik layanan kecuali disepakati lain.
8. Uji memakai input yang sama dan kondisi terkontrol. Hasil tidak digeneralisasi ke seluruh perangkat/model.
9. Audio dan citra diproses lokal; penyimpanan data wajah/tubuh dibatasi sesuai kebutuhan dan kebijakan privasi.
10. Angka target PoC adalah target penerimaan yang perlu diverifikasi, bukan hasil penelitian.

## 1.4 Tujuan Penelitian

1. Mengembangkan gateway, UI, dan orkestrator berbasis microservices dengan kontrak API yang konsisten.
2. Mengimplementasikan registry, pemeriksaan status, load/unload model, manajemen mode, dan pencatatan sumber daya GPU.
3. Membandingkan strategi all-resident, naive load/unload, pinned-memory swap, dan prefetch menggunakan metrik yang dapat diukur.
4. Mengevaluasi perpindahan mode, penanganan kegagalan, dan kestabilan operasi kiosk.

## 1.5 Manfaat Penelitian

**Akademis:** menyediakan studi implementasi dan evaluasi orkestrasi layanan AI pada edge device dengan VRAM terbatas.  
**Praktis:** menyediakan dasar integrasi beberapa layanan AI melalui kontrak API, registry, dan lifecycle terpusat.  
**Pengembangan sistem:** membantu mengidentifikasi trade-off latensi/memori, batas model, serta kebutuhan perangkat keras dan runtime.

# 5. Draf revisi Bab II — Tinjauan Pustaka

## 2.1 Penelitian Terdahulu

### 2.1.1 MiniDeep: A Standalone AI-Edge Platform with a Deep Learning-Based MINI-PC and AI-QSR System

MiniDeep membahas platform AI-edge yang menggabungkan perangkat komputasi lokal dan layanan aplikasi berbasis deep learning. Relevansinya terletak pada penerapan AI pada perangkat edge dengan sumber daya terbatas dan integrasi komponen perangkat lunak untuk fungsi interaktif. Penelitian ini dapat menjadi landasan untuk membahas penggunaan perangkat lokal sebagai lingkungan inferensi. Perbedaan penelitian ini adalah fokus pada orkestrasi beberapa layanan AI heterogen yang berbagi satu GPU dan pengukuran strategi lifecycle model.

### 2.1.2 SensiX++: Bringing MLOps and Multi-Tenant Model Serving to Sensory Edge Devices

SensiX++ membahas penyajian beberapa model pada perangkat edge dengan perhatian terhadap manajemen model, isolasi, dan efisiensi serving. Relevansinya adalah kebutuhan mengelola model dengan karakteristik berbeda pada sumber daya yang terbatas. Penelitian ini berbeda karena berfokus pada satu smart kiosk dengan mode interaksi berbeda, termasuk pipeline model berurutan, proses yang perlu berjalan bersamaan, dan mode visual eksklusif.

### 2.1.3 Exploring GPU Sharing Techniques for Edge AI Smart City Applications

Penelitian ini relevan karena mengevaluasi teknik berbagi GPU untuk workload AI pada perangkat edge dan memperhatikan kinerja serta pemanfaatan sumber daya. Aspek tersebut mendukung pemilihan metrik seperti penggunaan memori dan latensi. Penelitian ini berbeda dalam konteks perangkat, pola interaksi, dan fokus pada lifecycle model serta transisi mode kiosk melalui gateway dan orkestrator.

### 2.1.4 Sintesis dan posisi penelitian

Penelitian terdahulu membahas AI-edge, serving beberapa model, dan pemanfaatan GPU. Posisi penelitian ini adalah mengintegrasikan layanan AI modular pada satu smart kiosk lokal dan mengevaluasi empat strategi pengelolaan model dalam batas VRAM 8 GB. Kontribusinya berupa implementasi dan evaluasi sistem pada konteks kiosk, bukan klaim menciptakan teknik GPU sharing baru.

## 2.2 Landasan Teori

### 2.2.1 Smart kiosk dan edge computing
Smart kiosk merupakan sistem interaktif yang menyediakan layanan melalui komputasi dan antarmuka mandiri. Inferensi lokal mengurangi ketergantungan pada jaringan eksternal, tetapi dibatasi oleh CPU, RAM, GPU, VRAM, dan penyimpanan perangkat.

### 2.2.2 Inferensi AI lokal
Inferensi adalah penggunaan model yang telah tersedia untuk menghasilkan keluaran dari input. Waktu membaca bobot, menginisialisasi runtime, memindahkan bobot, dan memproses input harus dipisahkan agar latensi dapat dianalisis dengan benar.

### 2.2.3 Microservices dan kontainerisasi
Microservices memisahkan tanggung jawab layanan dan menghubungkannya melalui API. Kontainerisasi mengemas dependensi dan lingkungan eksekusi, tetapi tidak otomatis berarti arsitektur sudah berbasis microservices; pemisahan tanggung jawab dan kontrak komunikasi tetap diperlukan.

### 2.2.4 Gateway, kontrak API, dan registry
Gateway menjadi pintu masuk UI. Kontrak layanan pada PoC meliputi `GET /health`, `POST /load`, `POST /unload`, `POST /infer` atau WebSocket, dan `GET /metrics`. Registry menyimpan ID model, endpoint, kebutuhan VRAM, mode, eksklusivitas, dependensi, dan metode lifecycle.

### 2.2.5 Orkestrasi dan manajemen VRAM
Orkestrator mengatur status, lifecycle model, perpindahan mode, routing, timeout, dan pemulihan. VRAM menampung bobot, aktivasi, cache, dan buffer runtime; penggunaan aktual dapat melebihi ukuran file model. Status unloaded harus didasarkan pada verifikasi proses dan memori, bukan hanya perintah stop yang telah dikirim.

### 2.2.6 Strategi pengelolaan model
**All-resident** mempertahankan model di VRAM untuk menekan waktu load tetapi membutuhkan memori besar. **Naive load/unload** memuat model saat diperlukan dan melepasnya setelah selesai, tetapi menambah waktu transisi. **Pinned-memory swap** memindahkan bobot dari pinned RAM ke VRAM, hanya bila runtime mendukungnya dan RAM cukup. **Prefetch** memuat model berikutnya sebelum diperlukan untuk mengurangi waktu tunggu, tetapi berpotensi menambah tekanan memori.

### 2.2.7 Mode kiosk dan metrik
Mode percakapan dapat melibatkan STT, LLM, TTS, dan avatar; rekomendasi busana melibatkan VLM lalu difusi gambar; try-on video dan photobooth dapat bersifat eksklusif. Metrik meliputi VRAM puncak, waktu load/unload/swap, latensi inferensi, waktu sampai token/audio pertama, keberhasilan, error, timeout, OOM, FPS, dan latensi kamera-ke-layar bila tersedia.

## 2.3 Kerangka Pemikiran

Masalah layanan AI heterogen pada GPU 8 GB ditangani dengan microservices, gateway, registry, dan orkestrator. Empat strategi pengelolaan model diuji menggunakan workload terkontrol. Penggunaan VRAM/RAM, waktu load/swap, latensi, keberhasilan, dan kegagalan dianalisis untuk menjelaskan trade-off serta batas penerapan strategi pada smart kiosk.

# 6. Draf revisi Bab III — Metodologi Penelitian

## 3.1 Metode yang Digunakan

Penelitian menggunakan metode pengembangan sistem yang dilanjutkan evaluasi eksperimental kuantitatif. Sistem dikembangkan untuk mengintegrasikan UI kiosk, gateway, orkestrator, dan layanan AI lokal melalui kontrak API. Evaluasi membandingkan strategi pengelolaan model pada GPU lokal, dengan pengukuran penggunaan VRAM/RAM, waktu load dan perpindahan, latensi, keberhasilan permintaan, serta kegagalan.

## 3.2 Bahan dan Peralatan yang Digunakan

### 3.2.1 Hardware

a. **Mini PC dan GPU:** ASRock DeskMeet sesuai inventaris PoC, CPU AMD Ryzen 5, RAM 16 GB, SSD 1 TB, dan GPU Gigabyte NVIDIA RTX 5060 Low Profile 8 GB VRAM. Model motherboard, RAM, PCIe, dan versi driver diverifikasi pada tahap awal.

b. **Layar sentuh:** layar potret yang digunakan untuk antarmuka kiosk. Ukuran dan resolusi aktual diverifikasi, termasuk koneksi HDMI dan USB sentuh ke Ubuntu.

c. **Kamera USB:** target awal 1080p/30 fps untuk input rekomendasi busana, try-on, dan photobooth; kemampuan aktual dicatat.

d. **Mikrofon USB:** digunakan untuk input STT, diutamakan dengan echo cancellation.

e. **Speaker/soundbar:** digunakan untuk output TTS; speaker layar dapat dipakai jika tersedia dan memadai.

f. **Pencahayaan dan pemasangan:** lampu LED opsional untuk konsistensi citra dan dudukan/penutup yang tidak menghalangi aliran udara.

### 3.2.2 Software

a. **Sistem operasi:** Ubuntu Desktop GNOME sesuai PoC; versi OS/kernel dicatat setelah verifikasi.

b. **UI kiosk:** web app potret pada Chromium mode kiosk sesuai PoC.

c. **Bahasa dan backend:** Python untuk gateway, orkestrator, benchmark, dan instrumentasi; FastAPI untuk REST API dan WebSocket. JavaScript/TypeScript dapat digunakan pada UI web sesuai framework yang dipilih tim.

d. **Komunikasi:** REST/HTTP untuk request-response dan WebSocket untuk streaming bila dibutuhkan.

e. **Pengelolaan proses:** Docker/Compose atau proses terpisah sesuai kompatibilitas runtime. Keputusan final mempertimbangkan isolasi dependensi, akses GPU, dan overhead memori.

f. **GPU:** driver NVIDIA dan runtime sesuai model; NVIDIA Container Toolkit digunakan jika kontainer perlu akses GPU. Versi CUDA/PyTorch/CTranslate2/llama.cpp ditetapkan setelah uji kompatibilitas.

g. **Framework AI:** implementasi STT, LLM, TTS, avatar, VLM, generasi gambar, try-on, dan photobooth dipilih bersama pemilik TA; setiap model diuji mandiri dan lisensinya dicatat.

h. **Pemantauan:** NVML/binding Python untuk metrik terprogram, `nvidia-smi` untuk verifikasi, serta pemantauan proses/container untuk CPU, RAM, dan log.

i. **Pencatatan:** Python, CSV/JSONL, dan log terstruktur untuk menyimpan timestamp, strategi, model, input ID, kondisi cache, metrik, status, dan error.

## 3.3 Urutan Pelaksanaan Penelitian

### 3.3.1 Verifikasi hardware dan lingkungan
Verifikasi motherboard, RAM, PCIe, GPU/VRAM, OS, driver, layar sentuh, kamera, mikrofon, speaker, suhu, dan daya. Jalankan setiap kandidat model secara mandiri untuk memastikan kompatibilitas dan mencatat baseline.

### 3.3.2 Memilih dan menguji implementasi model
Pilih model yang mendukung inferensi lokal, sesuai fungsi layanan, kompatibel dengan GPU, dan memiliki lisensi yang dapat digunakan. Catat waktu load, latensi, RAM, VRAM puncak, dependensi, dan keberhasilan. Uji try-on video sejak awal karena berisiko tinggi pada 8 GB VRAM.

### 3.3.3 Merancang arsitektur dan kontrak API
Pisahkan UI, gateway, orkestrator, registry, dan proses layanan. Tetapkan endpoint health/load/unload/infer/metrics, format request-response, status, timeout, dan error. Registry memuat estimasi VRAM, mode, eksklusivitas, dan dependensi setiap proses model.

### 3.3.4 Mengimplementasikan gateway dan orkestrator
Bangun routing, health check, load/unload, readiness timeout, pencatatan log, dan penanganan kegagalan. Implementasikan naive load/unload sebagai baseline. Verifikasi proses yang berhenti dan amati VRAM setelah unload.

### 3.3.5 Mengimplementasikan strategi model
Implementasikan all-resident, naive load/unload, pinned-memory swap, dan prefetch sesuai dukungan runtime. Pisahkan cold load dan warm load. Jika pinned-memory tidak didukung, laporkan sebagai keterbatasan dan jangan mengklaim strategi telah diuji.

### 3.3.6 Mengimplementasikan registry dan kebijakan mode
Definisikan kombinasi model untuk percakapan, rekomendasi busana, try-on, dan photobooth. Atur model yang perlu berjalan bersamaan, model yang harus dilepas sebelum model eksklusif diaktifkan, dan mekanisme keluar dari mode eksklusif.

### 3.3.7 Membangun benchmark dan mengumpulkan data
Gunakan input audio/gambar yang sama, kondisi awal terdokumentasi, warm-up terpisah, dan mulai dengan 10 pengulangan per kondisi. Catat timestamp, VRAM/RAM, load/unload/swap, latensi, keberhasilan, OOM, error, dan timeout. Jalankan 100 giliran percakapan untuk target PoC.

### 3.3.8 Membandingkan strategi
Bandingkan hasil strategi dengan workload dan model identik sejauh memungkinkan. Jika all-resident menggunakan model lebih kecil, pisahkan analisis profil sistem dari perbandingan strategi murni. Laporkan kegagalan dan kondisi tidak muat VRAM sebagai hasil.

### 3.3.9 Integrasi layanan dan UI kiosk
Integrasikan layanan visual melalui kontrak yang sama. Uji transisi percakapan → rekomendasi busana → try-on → photobooth → percakapan tanpa restart. Integrasikan UI web potret dengan status loading, progres, hasil, error, dan pemulihan.

### 3.3.10 Uji kestabilan dan analisis
Jalankan demo penuh dan uji stabilitas hingga delapan jam sesuai target PoC. Validasi data, hitung statistik deskriptif dan persentil bila sampel memadai, lalu analisis trade-off antara memori, latensi, keberhasilan, dan stabilitas. Kesimpulan harus didasarkan pada hasil terukur, bukan target awal.

# 7. Referensi awal

Periksa metadata dan isi publikasi asli sebelum penyerahan final.

[1] Y.-S. Chen, K.-H. Cheng, C.-S. Hsu, and H.-L. Zhang, “MiniDeep: A standalone AI-edge platform with a deep learning-based MINI-PC and AI-QSR system,” *Sensors*, vol. 22, no. 16, Art. no. 5975, 2022, doi: 10.3390/s22165975.

[2] M. D. Hossain et al., “The role of microservice approach in edge computing: Opportunities, challenges, and research directions,” *ICT Express*, vol. 9, no. 6, pp. 1162–1182, 2023, doi: 10.1016/j.icte.2023.06.006.

[3] V. Velepucha and P. Flores, “A survey on microservices architecture: Principles, patterns and migration challenges,” *IEEE Access*, vol. 11, pp. 88339–88358, 2023, doi: 10.1109/ACCESS.2023.3305687.

[4] C. Min, A. Mathur, U. G. Acer, A. Montanari, and F. Kawsar, “SensiX++: Bringing MLOps and multi-tenant model serving to sensory edge devices,” *ACM Transactions on Embedded Computing Systems*, vol. 22, no. 6, Art. no. 98, 2023, doi: 10.1145/3617507.

[5] S. Woo, J. Yeo, J. Kim, and K. Lee, “Exploring GPU sharing techniques for edge AI smart city applications,” *ETRI Journal*, vol. 47, no. 5, pp. 855–864, 2025, doi: 10.4218/etrij.2025-0065.

# 8. Keputusan yang harus dikunci

1. Konfirmasi UI web + Chromium kiosk atau setujui perubahan ke Flutter.
2. Tetapkan runtime dan versi model yang benar-benar berjalan pada GPU.
3. Pastikan strategi pinned-memory dapat diimplementasikan sebelum menjadikannya eksperimen inti.
4. Definisikan registry per proses/model, bukan hanya per fitur.
5. Sepakati anggaran VRAM avatar + TTS/LLM.
6. Uji kelayakan try-on video sejak awal dan sepakati fallback bersama tim.
7. Tetapkan metrik utama TA Rendy: VRAM puncak, load/unload/swap, latensi, keberhasilan, OOM/error/timeout, dan transisi mode.
8. Sepakati target angka dengan pembimbing; angka PoC adalah target awal, bukan hasil.
9. Tetapkan kebijakan privasi audio/citra pengguna.
10. Tegaskan bahwa kontribusi adalah orkestrasi dan evaluasi lifecycle model, bukan GPU scheduler tingkat kernel.

**Langkah terdekat:** mulai dari M0. Verifikasi hardware, jalankan satu model secara lokal, dan buat pencatatan VRAM serta waktu load/inferensi. Baru setelah itu finalisasi runtime, kontrak API, dan desain eksperimen.
