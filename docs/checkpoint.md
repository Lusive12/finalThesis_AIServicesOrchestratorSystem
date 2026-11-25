# checkpoint.md — Status Pelaksanaan & Tracking Progres TA

Dokumen ini melacak status aktif tugas, checklist pekerjaan, file yang disentuh, hasil verifikasi, serta langkah berikutnya.

> **Hubungan Antar-Dokumen:**
> - Master context proyek & panduan navigasi merujuk ke [AGENT.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/AGENT.md).
> - Batasan ruang lingkup & guardrail AI di [docs/guardrail.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/guardrail.md).
> - Keputusan teknis dan arsitektur dicatat di [docs/decisions.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/decisions.md).
> - Definisi operasional, rumus, dan batas 5 metrik evaluasi di [docs/metrics.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/metrics.md).
> - Rencana milestone dan Bab IV di [docs/evaluation_plan.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/evaluation_plan.md).
> - Peta jalan riset M0–M4 di [docs/research_roadmap.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/research_roadmap.md).
> - Alur kerja dan pipeline 3 tugas besar di [docs/pipeline.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/pipeline.md).
> - Panduan manual eksekusi sistem & troubleshooting di [docs/runbook.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/runbook.md).

---

## 1. Status Kerja Aktif

- **Fase Saat Ini:** Fase 2 — Kesiapan Audit Hardware (M0) & Perancangan Core Orchestrator (M2)
- **Target Segera:** Eksekusi audit fisik hardware (M0) dan uji baseline mandiri model AI (M1/M2).
- **Tanggal Diperbarui:** 18 November 2026

---

## 2. Milestone Tracking (M0 - M4)

| Milestone | Deskripsi | Status | Rujukan Panduan Eksekusi |
|---|---|---|---|
| **M0** | Verifikasi hardware (PCIe Gen4, RAM DDR5, GPU 8GB) & kelayakan mandiri model AI | `PLANNED` | [docs/implementation/01_HARDWARE_AUDIT_M0.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/01_HARDWARE_AUDIT_M0.md) |
| **M1** | Baseline pipeline suara lokal (STT → LLM → TTS) & kontrak adapter seragam | `PLANNED` | [docs/implementation/02_MODEL_INTEGRATION_M0_M1.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/02_MODEL_INTEGRATION_M0_M1.md) |
| **M2** | Orchestrator minimal (State machine, services.yaml, REST/WebSocket API, 4 strategi GPU) | `IN_PROGRESS` | [docs/implementation/03_ORCHESTRATOR_CORE_M2.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/03_ORCHESTRATOR_CORE_M2.md) & [04_RESOURCE_MANAGEMENT_M2.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/04_RESOURCE_MANAGEMENT_M2.md) |
| **M3** | Integrasi layanan visual & penanganan Exclusive GPU Mode (Try-on, Photobooth) | `PLANNED` | [docs/implementation/05_EXCLUSIVE_MODE_M3.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/05_EXCLUSIVE_MODE_M3.md) |
| **M4** | Kiosk Web UI (Portrait 9:16) pada Chromium Kiosk & uji benchmark 100 giliran | `IN_PROGRESS` | [docs/implementation/06_KIOSK_UI_M4.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/06_KIOSK_UI_M4.md) & [07_BENCHMARK_EVALUATION.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/implementation/07_BENCHMARK_EVALUATION.md) |

*Status yang valid: `PLANNED` | `IN_PROGRESS` | `IMPLEMENTED` | `TESTED` | `VALIDATED`*

---

## 3. Checklist Tugas Terperinci

### Tahap 1: Fondasi Dokumentasi & Standar Proyek
- [x] Sinkronisasi master context dari PoC, draft revisi, dan implementasi.
- [x] Pembuatan [docs/checkpoint.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/checkpoint.md).
- [x] Pembuatan [docs/decisions.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/decisions.md).
- [x] Pembuatan & Finalisasi [docs/metrics.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/metrics.md) menjadi 5 metrik evaluasi inti.
- [x] Restrukturisasi repositori modular (pemisahan `configs/`, `docs/`, `src/`, `results/`, `experiments/`).
- [x] Pembuatan dokumen baru: `evaluation_plan.md`, `research_roadmap.md`, `pipeline.md`, `runbook.md`, `guardrail.md`.
- [x] Pembuatan konfigurasi YAML: `configs/services.yaml`, `configs/modes.yaml`, `configs/benchmark.yaml`.
- [x] Implementasi modular `src/kiosk_ui/`, `src/orchestrator/`, `src/resource_mgmt/`.
- [x] Pembuatan harness otomatis `run.py`, `experiments/runlog.py`, `experiments/run_benchmark.py`.

### Tahap 2: Audit Hardware & Baseline Uji Mandiri Model (M0)
- [ ] Audit hardware Mini PC via SSH (`dmidecode`, `lspci`, `nvidia-smi`, `libinput`).
- [ ] Catat hasil audit hardware pada [docs/decisions.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/decisions.md).
- [ ] Uji mandiri model STT (Faster-Whisper), ukur VRAM puncak & load time.
- [ ] Uji mandiri model LLM (Qwen/Llama GGUF via llama.cpp/Ollama), ukur VRAM puncak & time-to-first-token.
- [ ] Uji mandiri model TTS (Piper TTS), ukur VRAM puncak & RTF.
- [ ] Uji coba awal model citra (Try-on Erdi & Photobooth Deva).

### Tahap 3: Implementasi & Integrasi Core Orchestrator (M2)
- [x] Buat struktur folder proyek (`src/orchestrator/`, `src/kiosk_ui/`, `src/resource_mgmt/`, `configs/`, `experiments/`).
- [x] Buat file konfigurasi layanan `configs/services.yaml` dan mode `configs/modes.yaml`.
- [x] Implementasikan State Machine Lifecycle (`STOPPED`, `STARTING`, `READY`, `STOPPING`, `ERROR`).
- [x] Implementasikan backend FastAPI dengan gateway REST/WebSocket.
- [x] Implementasikan modul sampling NVML (`pynvml`) untuk VRAM dan RAM secara terprogram.
- [ ] Verifikasi sambungan end-to-end ke service model AI aktual saat hardware lab aktif.

---

## 4. Kendala / Blockers Saat Ini
- Belum ada sesi koneksi SSH langsung ke mesin Linux Lab target untuk eksekusi audit hardware nyata (`M0`).
- Model Try-on video berisiko tinggi terhadap kapasitas 8 GB VRAM; fallback path terdefinisi di `configs/modes.yaml`.
