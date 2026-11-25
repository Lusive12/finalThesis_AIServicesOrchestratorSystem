# Rencana Implementasi & Diagram Alur Empat Strategi Pengelolaan Model (Bab III)

Dokumen ini memuat perancangan alur kerja (*workflow/flowchart*) implementasi untuk **empat strategi pengelolaan siklus hidup model dan sumber daya GPU** pada Bab III Metodologi Penelitian. Seluruh diagram dirancang mengikuti kaidah visual naskah skripsi pada [writing.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/writing.md), definisi metrik pada [METRICS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/METRICS.md), serta batasan arsitektur pada [DECISIONS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/DECISIONS.md).

---

## Ringkasan Perbandingan Karakteristik 4 Strategi

| Strategi | Lokasi Bobot saat Idle | Mekanisme saat Permintaan Datang | Kebutuhan Host RAM | Kebutuhan GPU VRAM | Ekspektasi Latensi Inferensi/Transisi |
|---|---|---|---|---|---|
| **(a) All-Resident** | VRAM GPU | Langsung inferensi (tanpa alokasi baru) | Rendah (hanya OS & backend) | Tinggi ($\sum \text{VRAM model} \le 7,5\text{ GB}$) | Terendah (tanpa *loading overhead*) |
| **(b) Naive Load/Unload** | Storage SSD / Disk | Baca dari Disk $\rightarrow$ Alokasi ke VRAM $\rightarrow$ Inferensi $\rightarrow$ Rilis VRAM | Rendah (tidak di-*cache* di RAM) | Rendah (hanya 1 model aktif pada satu waktu) | Tertinggi (terbebani I/O Disk & inisialisasi) |
| **(c) Pinned-Memory Swap** | Host RAM (*Pinned Memory*) | Salin memori via bus PCIe (Host-to-Device) $\rightarrow$ Inferensi $\rightarrow$ Rilis VRAM | Tinggi ($\sum \text{Bobot model} \le \text{RAM}$) | Dinamis (1 model aktif pada satu waktu) | Menengah (kecepatan PCIe 16–32 GB/s) |
| **(d) Prefetch** | Host RAM & VRAM Bersebelahan | Pemuatan tumpang tindih (*overlap*) sebelum model aktif selesai | Tinggi (RAM + VRAM pasangan model) | Menengah ($V_{\text{aktif}} + V_{\text{berikutnya}} \le 7,5\text{ GB}$) | Mendekati Strategi (a) dengan kapasitas model lebih besar |

---

## 1. Strategi (a): Semua Model Tetap Dimuat (All-Resident)

### 1.1 Penjelasan Operasional
Pada strategi ini, seluruh model AI yang diperlukan dimuat ke dalam VRAM GPU saat inisialisasi awal sistem (*startup*) dan dipertahankan (*resident*) secara permanen. Agar tidak melampaui batas 8 GB VRAM, model yang dipilih menggunakan varian bobot yang lebih ringkas (misal: model terkuantisasi intensif atau arsitektur parameter lebih kecil). Saat pengguna berinteraksi, orkestrator langsung meneruskan payload ke model yang sudah berada dalam status `READY`.

### 1.2 Flowchart Implementasi
```mermaid
flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Inisialisasi Sistem Kiosk]) --> B[Orkestrator Membaca services.yaml]
    B --> C[Alokasikan Seluruh Model AI Sekaligus ke VRAM GPU<br/>Model 1 + Model 2 + Model N]:::gpu
    C --> D{Apakah Total VRAM <= 7,5 GB?}:::cond
    D -- Tidak --> E[Peringatan: Risiko CUDA OOM<br/>Ganti ke Model Lebih Kecil / Gagal]:::startEnd
    D -- Ya --> F[Semua Layanan Berstatus READY]:::orch

    F --> G([Menunggu Permintaan Pengguna]):::startEnd
    G --> H[Permintaan Masuk: Audio / Teks Masuk]
    H --> I[Orkestrator Meneruskan Input Langsung ke Model Terkait]:::orch
    I --> J[Inferensi Dijalankan pada VRAM GPU Aktif]:::gpu
    J --> K[Kirim Hasil Inferensi ke UI Kiosk]
    K --> L[Model Tetap Dipertahankan di VRAM GPU]:::gpu
    L --> G
```

---

## 2. Strategi (b): Pemuatan dan Pelepasan Naif (Naive Load/Unload)

### 2.1 Penjelasan Operasional
Strategi ini mengadopsi prinsip penggunaan sumber daya minimal pada satu waktu (*just-in-time loading*). Seluruh bobot model tersimpan pada media penyimpanan lokal (SSD). Saat suatu layanan dipanggil:
1. Model dimuat dari disk ke memori GPU.
2. Inferensi diproses.
3. Setelah selesai menghasilkan respons, model segera di-*unload* dan proses/alokasi VRAM dilepaskan kembali hingga mendekati nilai *baseline* sebelum melayani tahap berikutnya.

### 2.2 Flowchart Implementasi
```mermaid
flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Permintaan Pengguna Diterima]) --> B[Orkestrator Menganalisis Layanan Target]:::orch
    B --> C{Apakah Ada Model Lain Aktif di VRAM?}:::cond
    C -- Ya --> D[Kirim Perintah Unload Model Aktif]:::orch
    D --> E[Tunggu Proses Berhenti & Polling NVML Hingga VRAM Rilis]:::gpu
    C -- Tidak --> F[Baca File Bobot Model Target dari Penyimpanan SSD]:::process
    E --> F

    F --> G[Muat Bobot ke VRAM GPU & Inisialisasi Konteks Model]:::gpu
    G --> H{Readiness Check Sukses?}:::cond
    H -- Tidak / Timeout --> I[Catat Error Log & Kembalikan Respons Gagal]:::startEnd
    H -- Ya --> J[Jalankan Inferensi pada Model]:::gpu
    J --> K[Kirim Hasil Inferensi ke Pengguna / UI]

    K --> L[Orkestrator Mengirim Perintah Unload Model]:::orch
    L --> M[Bebaskan VRAM GPU & Hancurkan Konteks Runtime]:::gpu
    M --> N([Selesai: VRAM Kembali ke Status Baseline]):::startEnd
```

---

## 3. Strategi (c): Pertukaran Memori Terpancang (Pinned-Memory Swap)

### 3.1 Penjelasan Operasional
Pada strategi ini, latensi I/O dari media penyimpanan (SSD) dieliminasi dengan mempertahankan bobot seluruh model di dalam **Host RAM yang dialokasikan sebagai Pinned (Page-Locked) Memory**. 
- Pinned memory mencegah sistem operasi melakukan *paging/swap* ke disk virtual, sehingga bus PCIe dapat melakukan transfer *Direct Memory Access* (DMA) langsung ke VRAM GPU dengan kecepatan penuh (mencapai ~15,8 GB/s pada PCIe 4.0 x8).
- Model dipindahkan ke VRAM saat dibutuhkan, dan saat selesai, alokasi VRAM dibebaskan kembali tanpa perlu membuang bobot dari Host RAM.

### 3.2 Flowchart Implementasi
```mermaid
flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Booting Sistem]) --> B[Muat Seluruh Bobot Model ke Host RAM Pinned Memory]:::process
    B --> C[Status: Seluruh Model Siap di Host RAM, VRAM GPU Kosong/Baseline]

    C --> D([Permintaan Layanan Diterima]):::startEnd
    D --> E[Orkestrator Mengirim Sinyal Swap-In Model Target]:::orch
    E --> F[Transfer Bobot Cepat via PCIe DMA: Host Pinned RAM -> GPU VRAM]:::gpu
    F --> G[Inisialisasi Konteks Inferensi di GPU]:::gpu
    
    G --> H{Kesiapan GPU Terverifikasi?}:::cond
    H -- Ya --> I[Eksekusi Inferensi Model pada GPU]:::gpu
    H -- Tidak --> J[Tangani Error Transfer PCIe]:::startEnd

    I --> K[Kirim Hasil Inferensi ke UI Kiosk]
    K --> L[Lepaskan VRAM GPU Model Tersebut]:::gpu
    L --> M[Bobot Tetap Bertahan Utuh di Host Pinned RAM]:::process
    M --> N([Selesai: VRAM Bersih, Menunggu Siklus Berikutnya]):::startEnd
```

---

## 4. Strategi (d): Pemuatan Awal Spekulatif (Prefetch)

### 4.1 Penjelasan Operasional
Strategi ini memanfaatkan ketergantungan sekuensial yang terprediksi pada alur interaksi kiosk (misal: saat Model N selesai memproses input, sistem hampir pasti mengeksekusi Model N+1).
- Total seluruh model mungkin tidak dapat ditampung bersamaan di VRAM 8 GB, namun **pasangan model bersebelahan muat secara simultan** dalam batas memori yang aman.
- Orkestrator memicu pemuatan awal (*prefetch*) model tahap berikutnya ke VRAM GPU secara asinkronus di latar belakang (*background thread*) ketika model tahap aktif sedang menyelesaikan inferensinya. Dengan demikian, waktu tunggu pemindahan memori tertutupi oleh waktu komputasi model aktif (*latency hiding*).

### 4.2 Flowchart Implementasi
```mermaid
flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Permintaan Layanan Masuk]) --> B[Model N Aktif: Inferensi Berjalan pada GPU]:::gpu
    B --> C[Orkestrator Mendeteksi Prediksi Alur: Model N+1 Siap Disiapkan]:::orch
    
    subgraph Parallel_Execution [Eksekusi Paralel / Overlap]
        direction TB
        D[Thread 1: Selesaikan Sisa Inferensi Model N]:::gpu
        E[Thread 2: Prefetch Bobot Model N+1 dari Host RAM ke VRAM GPU]:::gpu
    end

    C --> Parallel_Execution
    D --> F[Hasil Inferensi Model N Siap Diteruskan ke Model N+1]
    E --> G{Apakah Model N+1 Sudah Ready di VRAM?}:::cond

    F --> H[Sinkronisasi Orkestrator: Handover Data Antar-Model]:::orch
    G -- Ya --> H
    G -- Belum --> I[Tunggu Prefetch Selesai: Minimal Delay]:::process
    I --> H

    H --> J[Kirim Perintah Background Unload untuk Model N yang Sudah Selesai]:::orch
    H --> K[Segera Eksekusi Inferensi Model N+1 Tanpa Menunggu Model N Selesai Dihapus]:::gpu
    K --> L[VRAM Model N Bebas Sepenuhnya]:::gpu
    L --> M([Lanjutkan Pola Prefetch ke Tahap Berikutnya N+2]):::startEnd
```

---

## 5. Hubungan dengan Pengujian dan Evaluasi Bab IV

1. **Metrik Terkait:** Waktu aktivasi, transisi, dan latensi inferensi dari keempat alur di atas akan dicatat secara otomatis menggunakan instrumen yang terdefinisi pada [METRICS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/METRICS.md) (`MTR-01` s.d. `MTR-07`).
2. **Kepatuhan Penulisan Naskah:** Format penulisan deskripsi alur pada Bab III wajib merujuk kaidah penulisan akademik dan ketentuan penyisipan gambar pada [writing.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/writing.md).
