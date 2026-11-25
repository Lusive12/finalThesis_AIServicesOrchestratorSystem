import urllib.request
import base64
from pathlib import Path

OUT_DIR = Path("assets/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Format Mermaid diagram yang bersih & valid
DIAGRAMS = {
    "strategi_a_all_resident.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Inisialisasi Sistem Kiosk]):::startEnd --> B[Orkestrator Membaca services.yaml]:::process
    B --> C[Alokasikan Semua Model Sekaligus ke VRAM GPU<br/>STT + LLM + TTS]:::gpu
    C --> D{Apakah Total VRAM &le; 7.5 GB?}:::cond
    D -- Tidak --> E[Peringatan: Risiko CUDA OOM<br/>Ganti ke Model Lebih Ringan / Gagal]:::startEnd
    D -- Ya --> F[Semua Layanan Berstatus READY]:::orch

    F --> G([Menunggu Permintaan Pengguna]):::startEnd
    G --> H[Permintaan Masuk: Audio / Teks Masuk]:::process
    H --> I[Orkestrator Meneruskan Input Langsung ke Model Terkait]:::orch
    I --> J[Inferensi Dijalankan pada VRAM GPU Aktif]:::gpu
    J --> K[Kirim Hasil Inferensi ke UI Kiosk]:::process
    K --> L[Model Tetap Dipertahankan di VRAM GPU]:::gpu
    L --> G
""",
    "strategi_b_naive_load_unload.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Permintaan Pengguna Diterima]):::startEnd --> B[Orkestrator Menganalisis Layanan Target]:::orch
    B --> C{Apakah Ada Model Lain Aktif di VRAM?}:::cond
    C -- Ya --> D[Kirim Perintah Unload Model Aktif]:::orch
    D --> E[Tunggu Proses Berhenti & Polling NVML Hingga VRAM Rilis]:::gpu
    C -- Tidak --> F[Baca File Bobot Model Target dari Penyimpanan SSD]:::process
    E --> F

    F --> G[Muat Bobot ke VRAM GPU & Inisialisasi Konteks Model]:::gpu
    G --> H{Readiness Check Sukses?}:::cond
    H -- Tidak / Timeout --> I[Catat Error Log & Kembalikan Respons Gagal]:::startEnd
    H -- Ya --> J[Jalankan Inferensi pada Model]:::gpu
    J --> K[Kirim Hasil Inferensi ke Pengguna / UI]:::process

    K --> L[Orkestrator Mengirim Perintah Unload Model]:::orch
    L --> M[Bebaskan VRAM GPU & Hancurkan Konteks Runtime]:::gpu
    M --> N([Selesai: VRAM Kembali ke Status Baseline]):::startEnd
""",
    "strategi_c_pinned_memory_swap.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Booting Sistem]):::startEnd --> B[Muat Seluruh Bobot Model ke Host RAM Pinned Memory]:::process
    B --> C[Status: Seluruh Model Siap di Host RAM, VRAM GPU Kosong / Baseline]:::process

    C --> D([Permintaan Layanan Diterima]):::startEnd
    D --> E[Orkestrator Mengirim Sinyal Swap-In Model Target]:::orch
    E --> F[Transfer Bobot Cepat via PCIe DMA: Host Pinned RAM -> GPU VRAM]:::gpu
    F --> G[Inisialisasi Konteks Inferensi di GPU]:::gpu
    
    G --> H{Kesiapan GPU Terverifikasi?}:::cond
    H -- Ya --> I[Eksekusi Inferensi Model pada GPU]:::gpu
    H -- Tidak --> J[Tangani Error Transfer PCIe]:::startEnd

    I --> K[Kirim Hasil Inferensi ke UI Kiosk]:::process
    K --> L[Lepaskan VRAM GPU Model Tersebut]:::gpu
    L --> M[Bobot Tetap Bertahan Utuh di Host Pinned RAM]:::process
    M --> N([Selesai: VRAM Bersih, Menunggu Siklus Berikutnya]):::startEnd
""",
    "strategi_d_prefetch.png": """flowchart TD
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef gpu fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px

    A([Mulai: Pengguna Selesai Berbicara]):::startEnd --> B[Model N Aktif: Inferensi STT Berjalan di GPU]:::gpu
    B --> C[Orkestrator Mendeteksi Prediksi Jalur: Model N+1 adalah LLM]:::orch
    
    subgraph Parallel_Execution [Eksekusi Paralel / Overlap]
        direction TB
        D[Thread 1: Selesaikan Sisa Inferensi Model N]:::gpu
        E[Thread 2: Prefetch Bobot Model N+1 dari Host RAM ke VRAM GPU]:::gpu
    end

    C --> Parallel_Execution
    D --> F[Hasil Inferensi Model N Siap Diteruskan ke Model N+1]:::process
    E --> G{Apakah Model N+1 Sudah Ready di VRAM?}:::cond

    F --> H[Sinkronisasi Orkestrator: Handover Data Antar-Model]:::orch
    G -- Ya --> H
    G -- Belum --> I[Tunggu Prefetch Selesai: Minimal Delay]:::process
    I --> H

    H --> J[Kirim Perintah Background Unload untuk Model N yang Sudah Selesai]:::orch
    H --> K[Segera Eksekusi Inferensi Model N+1 Tanpa Menunggu Model N Selesai Dihapus]:::gpu
    K --> L[VRAM Model N Bebas Sepenuhnya]:::gpu
    L --> M([Lanjutkan Pola Prefetch ke Tahap Berikutnya N+2]):::startEnd
"""
}

for filename, code in DIAGRAMS.items():
    b64 = base64.urlsafe_b64encode(code.strip().encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{b64}?bgColor=!white"
    out_file = OUT_DIR / filename
    print(f"Mengunduh & merender {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out_file.write_bytes(resp.read())
    print(f"-> Berhasil dibuat: {out_file} ({out_file.stat().st_size} bytes)")
