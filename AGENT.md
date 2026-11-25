# AGENT.md — Context Hub & Policy: Smart Kiosk AI Orchestration

**Judul Tugas Akhir:** Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk  
**Pemilik TA:** Rendy Lexxy Kurniawan (NRP 5024231007)  
**Departemen:** Teknik Komputer, FTEIC, Institut Teknologi Sepuluh Nopember (ITS)  
**Platform Target:** Mini PC ASRock DeskMeet (Ubuntu Linux), 1 GPU NVIDIA RTX 5060 8 GB VRAM.

---

## 0. Protokol Memulai Sesi Kerja (AI Agent Protocol)

1. **Hemat Konteks & Jangan Baca Semua Dokumen:** Repositori ini telah direstrukturisasi secara modular. Baca **HANYA** file yang relevan dengan tugas spesifik Anda saat ini (lihat *Peta Navigasi Dokumen* di bawah).
2. **Periksa Status Aktif Sebelum Bekerja:** Buka [docs/checkpoint.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/checkpoint.md) untuk melihat milestone berjalan, tugas aktif, dan blocker.
3. **Patuhi Batasan:** Baca [docs/guardrail.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/guardrail.md). Jangan mengarang data benchmark, jangan memodifikasi judul, dan jangan menjalankan perintah terminal destruktif (`pkill -f`).
4. **Catat Keputusan Baru:** Setiap keputusan teknis, arsitektur, atau runtime wajib dicatat pada [docs/decisions.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/decisions.md) (format `ADR-xxx`).
5. **Perbarui Checkpoint Saat Selesai:** Selalu centang tugas selesai dan perbarui daftar langkah berikutnya di `docs/checkpoint.md`.

---

## 1. Peta Navigasi Dokumen (Zero-Context-Bloating Matrix)

| Kategori Kebutuhan Anda | Dokumen Otoritatif Tunggal yang Harus Dibaca |
|---|---|
| **Status Pekerjaan, Checklist & Blocker** | 👉 [docs/checkpoint.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/checkpoint.md) |
| **Log Keputusan Teknis & Arsitektur (ADR)** | 👉 [docs/decisions.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/decisions.md) |
| **Definisi 5 Metrik Evaluasi & Rumus Matematis** | 👉 [docs/metrics.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/metrics.md) |
| **Spesifikasi Detail Hardware & Software (Tech Stack)** | 👉 [docs/tech_stack.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/tech_stack.md) |
| **Rencana Evaluasi & Pemetaan ke Bab IV Skripsi** | 👉 [docs/evaluation_plan.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/evaluation_plan.md) |
| **Peta Jalan Riset Milestone M0–M4** | 👉 [docs/research_roadmap.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/research_roadmap.md) |
| **Alur Komunikasi & Pipeline 3 Tugas Besar** | 👉 [docs/pipeline.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/pipeline.md) |
| **Panduan Menjalankan Sistem, Benchmark & Debugging** | 👉 [docs/runbook.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/runbook.md) |
| **Batasan Ruang Lingkup & Larangan Keras AI** | 👉 [docs/guardrail.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/guardrail.md) |
| **Kontrak API Seragam Microservices AI** | 👉 [docs/architecture/api_contract.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/architecture/api_contract.md) |
| **Arsitektur Umum Sistem (Formal & Analogi)** | 👉 [docs/architecture/architecture_overview.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/architecture/architecture_overview.md) |
| **Perbandingan 4 Strategi Pengelolaan GPU** | 👉 [docs/architecture/strategy_comparison.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/architecture/strategy_comparison.md) |
| **Pedoman Penulisan Laporan & Sitasi IEEE** | 👉 [docs/writing/writing_guide.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/writing/writing_guide.md) |
| **Standar Visual Diagram & Ekspor PNG 300 DPI** | 👉 [docs/writing/diagram_guide.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/writing/diagram_guide.md) |
| **Panduan Slide Presentasi Seminar Proposal** | 👉 [docs/writing/ppt_guide.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/writing/ppt_guide.md) |
| **Naskah LaTeX Resmi Bab 3 & Bibliografi** | 👉 [docs/bab3_latex/](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/bab3_latex/) |
| **Panduan Implementasi Teknis Bertahap (M0–M4)** | 👉 [docs/implementation/](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/) |
| **Material Referensi & Analisis TA Teman** | 👉 [docs/references/](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/references/) |

---

## 2. Struktur Repositori Utama

```text
proof-concept-smartkiosk/
├── AGENT.md                  # Navigasi utama & protokol agen (file ini)
├── run.py                    # Unified CLI: server, kiosk, benchmark, audit-hardware
├── requirements.txt          # Dependensi Python ter-pin
├── configs/                  # services.yaml, modes.yaml, benchmark.yaml
├── docs/                     # Dokumentasi terkelompok fungsi (lihat tabel di atas)
├── src/                      # Source code 3 Tugas Besar
│   ├── kiosk_ui/             # TB 1: UI/UX Chromium Kiosk (HTML5/CSS/JS portrait 9:16)
│   ├── orchestrator/         # TB 2: FastAPI Gateway, Registry, Lifecycle State Machine
│   └── resource_mgmt/        # TB 3: 4 Strategi GPU, VRAM Barrier, PyNVML Sampler
├── experiments/              # Harness benchmark terotomasi & runlog.py (provenance)
├── results/                  # Rekaman log CSV, JSONL, dan artefak pengujian
└── assets/diagrams/          # Gambar diagram PNG resolusi tinggi (300 DPI)
```

---

## 3. Prioritas Kerja Saat Ini
Untuk melihat tugas aktif dan prioritas langsung pengujian, silakan buka:  
👉 **[docs/checkpoint.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/checkpoint.md)**
