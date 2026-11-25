# METODOLOGI_PENELITIAN_BAB3.md — Urutan Pelaksanaan Penelitian (Bab 3.3)

Dokumen ini memuat draf revisi resmi untuk **Subbab 3.3 Urutan Pelaksanaan Penelitian** pada naskah skripsi Bab III Tugas Akhir:  
**“Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk”** (Rendy Lexxy Kurniawan - NRP 5024231007).

Dokumen ini disusun menyelaraskan rencana draf lama dengan keputusan terbaru pada [AGENT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/AGENT.md), PoC revisi A [given_materials/PROOF_OF_CONCEPT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/given_materials/PROOF_OF_CONCEPT.md), keputusan arsitektur [DECISIONS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/DECISIONS.md), dan 5 metrik evaluasi resmi pada [METRICS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/METRICS.md).

---

## Evaluasi Kritis terhadap Draf Lama

Draf lama Anda memiliki alur dasar yang baik, namun terdapat **4 kelemahan fatal** yang bertentangan dengan keputusan dosen pembimbing dan PoC terbaru:

1. **Stack UI Kiosk Masih Menggunakan Flutter Desktop:**
   - *Masalah:* Draf lama menyebutkan Flutter pada 3.3.3 dan 3.3.5. Padahal, PoC terbaru dan ADR-001 secara resmi menetapkan **Web Application yang dijalankan pada Chromium fullscreen Kiosk mode**. Flutter rentan konflik display server Linux dengan driver NVIDIA dan streaming video.
2. **Skenario Pengujian Ketinggalan Zaman (Hanya Skenario A vs B):**
   - *Masalah:* Draf lama di 3.3.7 hanya membandingkan "aktif bersamaan vs aktif bergantian". Padahal kesepakatan terbaru menguji **4 Strategi Terkontrol**: (a) All-Resident, (b) Naive Load/Unload, (c) Pinned-Memory Swap, dan (d) Prefetch.
3. **Penyebutan Metrik Masih Campur Aduk:**
   - *Masalah:* Belum sinkron dengan 5 pilar metrik resmi yang sudah disepakati (Total/Average Latency, Swap Time, Inference Time, Peak VRAM, dan Stability Rate).
4. **Tahap Verifikasi Hardware Awal Belum Ada:**
   - *Masalah:* Di lapangan, hardware Mini PC (X600 vs X300, PCIe 4.0 vs 3.0, driver Blackwell RTX 5060, layar sentuh) harus diaudit terlebih dahulu (*Milestone M0*) sebelum model dijalankan.

---

## Naskah Lengkap Subbab 3.3 (Siap Digunakan pada Laporan Skripsi)

```markdown
3.3 Urutan Pelaksanaan Penelitian

Pelaksanaan penelitian ini dilakukan melalui pendekatan rekayasa perangkat lunak sistem yang dilanjutkan dengan evaluasi eksperimental kuantitatif pada perangkat keras aktual. Tahapan penelitian dibagi menjadi delapan langkah sistematis sebagaimana diilustrasikan pada diagram alur penelitian, dimulai dari verifikasi lingkungan perangkat keras hingga analisis data hasil pengujian.

3.3.1 Verifikasi Perangkat Keras dan Lingkungan Sistem
Tahap awal dilakukan dengan memverifikasi spesifikasi fisik perangkat komputasi edge dan periferal kios cerdas. Verifikasi mencakup pemeriksaan arsitektur motherboard (ASRock DeskMeet), generasi dan jalur antarmuka PCIe, kapasitas serta tipe modul RAM (DDR5), versi driver grafis NVIDIA pendukung arsitektur Blackwell, pustaka CUDA, serta ketersediaan sistem operasi Linux Ubuntu. Selain unit komputasi, dilakukan pula pengujian fungsionalitas periferal masukan dan keluaran yang meliputi antarmuka layar sentuh potret 32 inci melalui koneksi HDMI dan USB sentuh, mikrofon USB array, kamera USB 1080p, dan pengeras suara. Tahap ini bertujuan memastikan seluruh komponen fisik dikenali oleh sistem operasi sebelum integrasi perangkat lunak dimulai.

3.3.2 Pemilihan dan Pengujian Mandiri Model AI
Model-model AI yang digunakan dalam penelitian ini tidak dilatih dari awal, melainkan memanfaatkan implementasi model siap pakai yang tersedia secara terbuka (open-weight) sesuai dengan domain interaksi kios cerdas. Pemilihan model didasarkan pada kesesuaian tugas, kompatibilitas runtime pada sistem operasi Linux dan GPU NVIDIA RTX 5060, kebutuhan memori VRAM, serta ketersediaan antarmuka pemanggilan lokal tanpa ketergantungan API komputasi awan. Setiap kandidat model diuji secara mandiri (standalone) di luar orkestrator untuk mencatat data dasar (baseline), yang meliputi konsumsi puncak VRAM saat proses inisialisasi dan inferensi, waktu pemuatan bobot (load time), serta waktu komputasi inferensi (inference time). Data baseline ini digunakan untuk menyusun batas anggaran alokasi memori pada registry layanan.

3.3.3 Perancangan Arsitektur Microservices dan Antarmuka Kios
Tahap ini merancang arsitektur sistem modular yang memisahkan tanggung jawab antarmuka pengguna, gateway, orkestrator, dan layanan model AI. Antarmuka kios dirancang sebagai aplikasi web berbasis tata letak potret berasio 9:16 yang dieksekusi melalui peramban Chromium dalam mode kios layar penuh (fullscreen kiosk mode). Komunikasi antara antarmuka dan backend dirancang menggunakan protokol HTTP REST API untuk perintah kontrol diskrit dan WebSocket untuk penyampaian status serta kejadian secara asinkronus. Pada lapisan backend, dirancang arsitektur orkestrator berbasis Python dan FastAPI yang dilengkapi dengan registry layanan (services.yaml), pendeteksi kesiapan model (readiness check), mekanisme transisi mode, serta modul pemantauan memori GPU berbasis NVIDIA Management Library (NVML).

3.3.4 Implementasi dan Kontainerisasi Layanan AI
Setiap model AI dibungkus menjadi modul layanan independen yang mengekspos kontrak antarmuka seragam, meliputi endpoint pemeriksaan kesehatan dan kesiapan (GET /health), instruksi pemuatan model (POST /load), instruksi pelepasan model (POST /unload), serta endpoint pemrosesan data (POST /infer). Lingkungan eksekusi dependensi model dikemas ke dalam proses terisolasi atau kontainer Docker dengan konfigurasi akses GPU menggunakan NVIDIA Container Toolkit. Pengujian mandiri dilakukan pada masing-masing layanan untuk memastikan proses penerimaan input, eksekusi inferensi, dan pelepasan memori video GPU dapat dikendalikan dengan benar melalui panggilan API lokal.

3.3.5 Pengembangan Orkestrator dan Modul Manajemen Sumber Daya
Pengembangan orkestrator difokuskan pada implementasi mesin status siklus hidup model (lifecycle state machine) yang mencakup status STOPPED, STARTING, READY, STOPPING, dan ERROR. Orkestrator dilengkapi logika penanganan mode eksklusif (exclusive GPU mode) untuk layanan berbasis visual berat yang membutuhkan alokasi VRAM dominan. Modul manajemen sumber daya (resource management) dibangun menggunakan pustaka pynvml untuk mencuplik alokasi VRAM secara terprogram dengan interval berkala 50–100 ms. Pada modul ini diimplementasikan empat strategi pengelolaan model yang akan dievaluasi:
a. Strategi All-Resident: mempertahankan seluruh model aktif di VRAM GPU.
b. Strategi Naive Load/Unload: memuat model dari media penyimpanan sekunder hanya saat dibutuhkan dan segera melepaskannya setelah inferensi selesai.
c. Strategi Pinned-Memory Swap: mempertahankan bobot model pada Host RAM (pinned memory) dan mentransfernya ke VRAM GPU melalui bus PCIe saat diperlukan.
d. Strategi Prefetch: memuat model tahap berikutnya secara asinkronus pada utas latar belakang (background thread) saat model aktif sedang memproses inferensi (latency hiding).

3.3.6 Integrasi Sistem dan Pengujian Fungsionalitas End-to-End
Seluruh komponen yang meliputi aplikasi web Chromium kios, API gateway, orkestrator, modul manajemen sumber daya, dan layanan-layanan AI diintegrasikan ke dalam satu kesatuan sistem kios cerdas. Pengujian fungsionalitas menyeluruh dilakukan melalui skenario alur pengguna (user flow) dari layar siaga (standby), pemilihan menu layanan, pengiriman input pengguna, pemantauan tampilan status pemuatan, hingga perolehan hasil keluaran. Pengujian integrasi ini secara khusus memverifikasi keandalan transisi antar-layanan tanpa memicu insiden memori GPU meluap (CUDA Out of Memory) serta memastikan sistem mampu pulih secara otomatis ke status siaga tanpa memerlukan booting ulang aplikasi jika terjadi kegagalan layanan.

3.3.7 Pengujian Kinerja dan Benchmark Komparatif
Pengujian kinerja dilakukan secara terkontrol menggunakan rangkaian data uji (workload) yang seragam dan diulang minimal 10 kali untuk setiap kondisi pengujian guna menjamin reprodusibilitas data. Pengujian membandingkan performa empat strategi pengelolaan model pada perangkat fisik yang sama. Data kinerja dicatat secara otomatis ke dalam berkas log terstruktur (CSV dan JSONL) berdasarkan 5 metrik evaluasi kinerja inti:
a. Total / Average Latency (Te2e): total jeda waktu dari akhir input pengguna hingga respons pertama dikeluarkan.
b. Waktu Swap dan Transisi Model (Tswap): waktu yang dihabiskan orkestrator untuk melepaskan model lama dan menyiapkan model baru hingga berstatus READY.
c. Waktu Inferensi Model (Tinfer): waktu komputasi murni model AI dalam memproses masukan saat model telah siaga di VRAM GPU.
d. Penggunaan VRAM Puncak (Vpeak): alokasi memori fisik GPU tertinggi yang tercatat selama eksekusi sistem terhadap batas target aman ≤ 7,5 GB.
e. Tingkat Kestabilan Sesi (Stability Rate): persentase keberhasilan sistem dalam menyelesaikan 100 giliran interaksi berturut-turut tanpa mengalami OOM, proses crash, atau timeout.

3.3.8 Analisis Data, Evaluasi Trade-off, dan Penyusunan Kesimpulan
Data kuantitatif yang terekam dari berkas log pengujian dikelompokkan berdasarkan strategi pengelolaan model dan dianalisis menggunakan metode statistik deskriptif, meliputi perhitungan nilai rata-rata (mean), median, simpangan baku (standard deviation), nilai minimum, dan nilai maksimum. Hasil pengukuran dianalisis untuk mengevaluasi trade-off rekayasa antara konsumsi memori VRAM GPU dan latensi respons sistem dari masing-masing strategi. Pembahasan difokuskan pada pembuktian apakah strategi alokasi dinamis (seperti Prefetch dan Pinned Swap) mampu menekan latensi mendekati strategi All-Resident namun tetap menjaga stabilitas memori di dalam batas 8 GB. Hasil analisis ini dijadikan dasar ilmiah dalam menarik kesimpulan penelitian dan merumuskan rekomendasi arsitektur orkestrasi pada perangkat kios cerdas masa depan.
```
