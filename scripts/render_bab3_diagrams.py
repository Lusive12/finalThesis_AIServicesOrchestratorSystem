import urllib.request
import base64
from pathlib import Path

OUT_DIR = Path("assets/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DIAGRAMS = {
    # DIAGRAM 1: Arsitektur Umum & Relasi Antar-Modul
    "bab3_01_arsitektur_umum.png": """flowchart LR
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef ui fill:#FEF9C3,stroke:#CA8A04,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef rm fill:#F3E8FF,stroke:#9333EA,stroke-width:2px
    classDef ai fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef eval fill:#FEE2E2,stroke:#DC2626,stroke-width:1.5px

    subgraph INP [1. Input Pengguna]
        U([Pengguna Kiosk]):::startEnd --> SENS[Sentuhan / Suara / Kamera]:::startEnd
    end

    subgraph TB1 [2. UI/UX Chromium Kiosk]
        SENS --> UI_PRES[Tampilan Layar Potret 9:16]:::ui
        UI_PRES --> UI_REQ[Kirim Permintaan Aksi Pengguna]:::ui
    end

    subgraph TB2 [3. Orchestrator]
        UI_REQ --> GW[API Gateway]:::orch
        GW --> ROUTE[Routing dan Seleksi Layanan]:::orch
        ROUTE --> STATE[Manajer Siklus Hidup Model AI]:::orch
    end

    subgraph TB3 [4. Resource Management]
        STATE <--> POLICY[Eksekusi Strategi Memori GPU]:::rm
        POLICY <--> MON[Pemantauan VRAM dan RAM via NVML]:::rm
    end

    subgraph AI_EXEC [5. Eksekusi Model AI]
        STATE --> INFER_EXEC[Inferensi Model AI pada GPU Lokal]:::ai
    end

    subgraph OUTP [6. Output dan Evaluasi]
        INFER_EXEC --> RES_DISP[Hasil Respons ke UI Kiosk]:::ui
        MON --> LOG_EVAL[Pencatatan 5 Metrik Evaluasi Kinerja]:::eval
    end
""",

    # DIAGRAM 2: User Flow Experience pada UI/UX Chromium Kiosk
    "bab3_02_alur_pengguna_ui.png": """flowchart LR
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef page fill:#FEF9C3,stroke:#CA8A04,stroke-width:1.5px
    classDef act fill:#E0F2FE,stroke:#0284C7,stroke-width:1.5px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px
    classDef res fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px

    A([Pengguna Mendekati Kiosk]):::startEnd --> B[Halaman Utama / Standby Screen]:::page
    B --> C{Pilih Menu Layanan}:::cond

    C -->|Percakapan Suara| D1[Halaman Percakapan Interaktif]:::page
    C -->|Rekomendasi Busana| D2[Halaman Kamera dan Analisis Busana]:::page
    C -->|Virtual Try-On| D3[Halaman Mode Video Cermin Langsung]:::page
    C -->|AI Photobooth| D4[Halaman Foto dan Hitung Mundur]:::page

    D1 --> E[Kirim Input Pengguna ke Gateway]:::act
    D2 --> E
    D3 --> E
    D4 --> E

    E --> F[Tampilan Loading dan Indikator Status]:::page
    F --> G{Pemeriksaan Kesiapan}:::cond

    G -- Berhasil Siap --> H[Tampilan Hasil Interaksi AI]:::res
    G -- Gagal atau Timeout --> I[Tampilan Pesan Penanganan Kendala]:::page

    H --> J{Selesai Interaksi?}:::cond
    I --> J
    J -- Lanjut Menu Lain --> B
    J -- Selesai --> K([Kembali ke Mode Standby]):::startEnd
""",

    # DIAGRAM 3: Metodologi & Alur Kerja Orchestrator
    "bab3_03_alur_kerja_orchestrator.png": """flowchart LR
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px
    classDef ready fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px

    A([Terima Permintaan dari UI]):::startEnd --> B[Validasi Format Pesan pada Gateway]:::orch
    B --> C[Baca Konfigurasi Layanan di Registry]:::orch
    C --> D{Perlu Pergantian Model Aktif?}:::cond

    D -- Ya --> E[Kirim Instruksi Unload Model Sebelumnya]:::orch
    E --> F[Verifikasi Konfirmasi Pembebasan Memori]:::process
    F --> G[Kirim Instruksi Load Model Target]:::orch
    G --> H{Pemeriksaan Kesiapan Model}:::cond

    D -- Tidak: Model Sudah Aktif --> I[Status Model Terverifikasi READY]:::ready
    H -- Berhasil --> I
    H -- Gagal / Timeout --> J[Catat Insiden Error dan Kirim Fallback]:::startEnd

    I --> K[Teruskan Payload ke Endpoint Inferensi]:::orch
    K --> L[Terima Respons Keluaran Model AI]:::process
    L --> M([Kirim Hasil Inferensi ke UI Kiosk]):::startEnd
""",

    # DIAGRAM 4: Metodologi & Alur Kerja Resource Management
    "bab3_04_alur_kerja_resource_management.png": """flowchart LR
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef process fill:#F9FAFB,stroke:#1F2937,stroke-width:1.5px
    classDef rm fill:#F3E8FF,stroke:#9333EA,stroke-width:2px
    classDef cond fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px
    classDef log fill:#FEE2E2,stroke:#DC2626,stroke-width:1.5px

    A([Sinyal Kebutuhan Alokasi GPU]):::startEnd --> B[Identifikasi Strategi Memori Terpilih]:::rm
    B --> C[Eksekusi Prosedur Alokasi dan Swap Memori]:::rm

    subgraph SIKLUS_PEMANTAUAN [Pemantauan Sumber Daya Terprogram]
        C --> D[Background Thread NVML Sampling 50-100 ms]:::process
        D --> E{Puncak VRAM Aman?}:::cond
        E -- Ya: VRAM Kurang dari 7.5 GB --> F[Verifikasi Batas Aman Terpenuhi]:::process
        E -- Tidak: VRAM Lebih dari 7.5 GB --> G[Peringatan Risiko OOM dan Mitigasi]:::rm
    end

    F --> H[Rekam Waktu Swap dan Waktu Inferensi]:::rm
    G --> H

    H --> I[Hitung Latensi Total dan Status Sesi]:::rm
    I --> J[Simpan 5 Metrik Evaluasi ke Log CSV atau JSONL]:::log
    J --> K([Data Siap Dianalisis pada Bab 4]):::startEnd
"""
}

for filename, code in DIAGRAMS.items():
    b64 = base64.urlsafe_b64encode(code.strip().encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{b64}?bgColor=!white"
    out_file = OUT_DIR / filename
    print(f"Mengunduh & merender {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=35) as resp:
        out_file.write_bytes(resp.read())
    print(f"-> Berhasil dibuat: {out_file} ({out_file.stat().st_size} bytes)")
