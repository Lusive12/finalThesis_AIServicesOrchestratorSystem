# Analisis Struktur Repo `TA_Ferdie_Prata` — Pelajaran untuk TA Rendy

> Dibuat 2026-11-18. Sumber: hasil membaca `/home/tugasakhir/TA_Ferdie_Prata` (**read-only, tidak ada file yang diubah**).
> Tujuan: merangkum apa yang dikerjakan di repo Ferdie dan pola apa yang layak ditiru untuk TA
> *"Sistem Orkestrasi Layanan AI Berbasis Microservices pada Sistem Smart Kiosk"*.

---

## 1. Gambaran Singkat TA Ferdie

**Judul:** Pengembangan Agen Percakapan Suara untuk Kiosk Layanan Informasi Menggunakan Pipeline STT, LLM Lokal, dan TTS.

- Meniru konsep **"Lisa" (UGM)**, tetapi hanya **backbone suara** (STT → RAG → LLM → TTS), **tanpa avatar**.
- Semua **lokal/offline** di PC lab RTX 5060 8 GB (sama dengan GPU target kiosk Rendy).
- Desain **client–server**: server FastAPI + WebSocket di PC lab, klien = browser (laptop via `ssh -L`, nanti layar kiosk).
- Status per 2026-11-18: benchmark Fase 1 selesai, pipeline end-to-end jalan di GPU
  (respons suara pertama median **1,49 s**, VRAM puncak gabungan **6,6 GB / 8 GB**), mode kiosk layar penuh sudah ada.

---

## 2. Struktur Direktori

```
TA_Ferdie_Prata/
├── CLAUDE.md            # instruksi untuk AI asisten: konteks, protokol kerja, konvensi kode
├── AGENT.md             # spesifikasi perilaku agen suara (persona, prompt, guardrail, turn-taking)
├── run.py               # MENU eksperimen: `python run.py <aksi>` → membungkus skrip di experiments/
├── requirements.txt     # dependensi utama (versi di-pin)
├── requirements-omnivoice.txt  # dependensi venv kedua untuk model yang bentrok
├── .gitignore           # audio di luar data/ diabaikan; data/ di-track sebagai bukti
├── configs/             # YAML: pipeline.yaml, benchmark.yaml, varian benchmark_stt_int8.yaml
├── docs/                # 12 dokumen "otak" proyek (lihat §3)
├── src/                 # kode produk (modular per komponen)
│   ├── stt/ llm/ tts/ rag/   # tiap modul punya antarmuka sederhana & bisa ditukar via config
│   ├── pipeline/        # orkestrator giliran percakapan (loop.py, config.py, sentences.py)
│   ├── server/          # FastAPI + WebSocket (/ws)
│   └── client/          # webapp (index.html, app.js, style.css) + kiosk.py (Firefox layar penuh)
├── experiments/         # skrip eksperimen per tahap uji
│   ├── runlog.py        # ★ pencatat run otomatis (meta.json, run.log, results.xlsx)
│   ├── gpu.py, gpu_monitor.py   # pengukuran VRAM/suhu/daya GPU
│   ├── worker_util.py   # menjalankan model di proses/venv terpisah
│   ├── t0_perangkat/    # uji webcam & mic
│   ├── t1_audio/        # jalur audio laptop ⇄ PC, analisis rekaman
│   ├── t2_stt/          # benchmark & analisis STT
│   ├── t3_llm/          # benchmark LLM, anotasi, penilaian buta
│   ├── t4_tts/          # benchmark & analisis TTS
│   ├── t5_pipeline/     # uji end-to-end (WebSocket), UI (Firefox headless), RAG
│   └── t6_vram/         # VRAM gabungan STT+LLM+TTS
├── data/                # INPUT eksperimen (di-track + README): recordings, stt, tts, questions, annotations
├── knowledge/           # dokumen knowledge base per cakupan (institut_contoh/*.md)
└── results/             # 95 folder run: <tanggal_jam>_<jenis>_<tag>/ + README.md
```

---

## 3. Isi Folder `docs/` (sistem dokumentasi)

| File | Fungsi | Dipakai untuk |
|---|---|---|
| `CHECKPOINT.md` | "Save point": tugas aktif (checkbox), langkah berikutnya, blocker, log selesai | Melanjutkan kerja antarsesi tanpa mulai dari nol |
| `RESEARCH_ROADMAP.md` | Konteks, rumusan masalah draft, arsitektur, fase riset, **mapping fase → bab laporan**, daftar tes awal T0–T6 | Perencanaan & Bab 1/3 |
| `DECISIONS.md` | Log keputusan `D-001…D-017` format *Konteks · Opsi · Keputusan · Alasan · Konsekuensi* | **Bahan langsung Bab 3** (justifikasi) |
| `EXPERIMENT_LOG.md` | Jurnal `EXP-000…EXP-071` + indeks tabel + **status bukti ✅/⚠️/❌** | Bab 4; hanya ✅ yang boleh dikutip |
| `METRICS.md` | Glosarium setiap metrik (definisi, rumus, arah ↑/↓, target, skrip) | Bab 2/3 (definisi metrik) |
| `EVALUATION_PLAN.md` | Metrik & metode evaluasi per komponen + end-to-end + biaya | Kerangka Bab 4 |
| `RUNBOOK.md` | Panduan langkah demi langkah menjalankan semua eksperimen + troubleshooting | Mahasiswa bisa mengulang sendiri |
| `TECH_STACK.md` | Hardware, kandidat model, **budget VRAM** | Bab 3 |
| `PIPELINE.md` | Arsitektur (diagram mermaid), protokol WebSocket, metrik per giliran, bukti uji | Bab 3/4 |
| `BENCHMARK_FINAL.md` | Rekap final STT/LLM/TTS + lokasi bukti | Bab 4 |
| `RUBRIK_LLM.md` | Rubrik penilaian manual (dikunci sebelum menilai) | Validitas penilaian |
| `WRITING_BRIEF.md` | Brief mandiri untuk AI penulis Bab 1–3: kerangka bab, angka yang boleh dikutip, referensi terverifikasi, format IEEE | Penulisan laporan |

---

## 4. Apa Saja yang Dikerjakan (ringkasan kronologis)

| Tahap | Isi | Contoh bukti |
|---|---|---|
| T0 Setup | PyTorch cu128 untuk RTX 5060 (Blackwell sm_120), cek GPU, uji webcam/mic | EXP-001, EXP-061/062 |
| T1 Audio | Rekam mic laptop lewat browser → PC lab; analisis level/SNR/clipping | EXP-007 |
| T2 STT | Benchmark 4 model Whisper; lalu Whisper vs Qwen3-ASR vs Parakeet pada 100 ujaran FLEURS-id + rekaman sendiri; **normalisasi ejaan Indonesia untuk WER** (D-006) | EXP-015, 027, 028, 040 |
| T3 LLM | Ollama: Qwen vs Gemma vs DeepSeek, 32 soal kampus, mode dengan/tanpa konteks; anotasi manual, **penilaian buta**, Cohen's kappa, replikasi | EXP-030, 041–043, 049+ |
| T4 TTS | Piper vs OmniVoice vs Supertonic; WER round-trip, UTMOS, prosodi F0, kemiripan penutur ECAPA | EXP-038, 039 |
| T5 Pipeline | Server FastAPI + WebSocket, RAG BM25, LLM streaming per kalimat → TTS; uji e2e, UI headless, kalibrasi RAG | EXP-052–056, 067 |
| T6 VRAM | Tiga konfigurasi model dimuat bersamaan → pilih STT int8 agar LLM 100 % di GPU (D-017) | EXP-063–065 |
| Kiosk | `run.py kiosk` → Firefox `--kiosk` di monitor LG; uji latensi suara pertama Supertonic vs Piper | EXP-069, 070 |

Temuan jujur yang juga dicatat: bug prompt (konteks RAG tidak terisi) → diperbaiki & run ulang dengan kontrol;
GPU Xid 79 saat beban penuh; RAG BM25 lemah terhadap parafrase berat (3/12) → dasar Fase 2.

---

## 5. Pola yang **Bagus dan Layak Ditiru**

### 5.1 Pencatatan eksperimen otomatis (`experiments/runlog.py`) ★ paling penting
Setiap run dibungkus `with Run("nama", args=..., inputs=...) as run:` dan otomatis menghasilkan
`results/<YYYYMMDD_HHMMSS>_<nama>_<tag>/` berisi:
- `meta.json` — perintah persis, argumen, **SHA-256 file input**, versi Python/paket, GPU & driver, git commit, status ok/error;
- `run.log` — salinan seluruh output terminal;
- hasil mentah (`results.csv`, `summary.json`, dll.) + `results.xlsx` gabungan untuk Excel.

Folder hasil **tidak pernah ditimpa/dihapus**; run cacat diberi `NOTE.md`.
Rantai bukti: *angka di Bab 4 → EXP-xxx → folder results/ → meta.json → SHA-256 input di data/*.

### 5.2 Protokol CHECKPOINT
Sebelum mengerjakan apa pun: tulis tugas + langkah checkbox di `CHECKPOINT.md`; centang tiap langkah selesai;
blocker dicatat lengkap dengan error. Sangat berguna bila bekerja dengan AI asisten lintas sesi.

### 5.3 Decision log → Bab 3 gratis
Setiap keputusan (pilih model, metrik, arsitektur) punya ID `D-xxx` dan alasan berbasis data eksperimen.

### 5.4 Status bukti ✅ / ⚠️ / ❌
Membedakan data yang sah dikutip dari smoke test atau run yang cacat — mencegah klaim angka tanpa bukti.

### 5.5 Satu pintu eksekusi: `run.py`
Menu interaktif + sub-perintah (`python run.py stt`, `python run.py pipeline`, ...). Mencetak perintah asli sebelum
dijalankan, sehingga tetap reprodusibel. Argumen sering dipakai punya **nilai default**.

### 5.6 Konfigurasi di YAML, bukan di kode
`configs/pipeline.yaml` memuat model, device, kuantisasi, parameter RAG/LLM/TTS, beserta komentar alasan (`D-0xx`, `EXP-0xx`).
Override saat runtime: `--set llm.model=...` (tercatat di `meta.json`).

### 5.7 Modul dengan antarmuka seragam & bisa ditukar
`transcribe()`, `retrieve()`, `stream()`, `synthesize()` — ganti model cukup ubah config.

### 5.8 Isolasi dependensi bentrok lewat worker
Model yang dependensinya bentrok dijalankan di venv terpisah (`.venv-omnivoice`) sebagai proses worker
(`worker_util.py`). Ini mirip konsep microservice.

### 5.9 Pengukuran GPU yang hati-hati
`gpu.py`/`gpu_monitor.py` mengukur VRAM via NVML dari luar proses; menghindari membuat konteks CUDA yang
"mencemari" pengukuran; monitor suhu/daya/clock selama sesi.

### 5.10 README di setiap folder data
`data/README.md`, `results/README.md`, `knowledge/<cakupan>/README.md` menjelaskan asal, format, lisensi, dan keterbatasan data.

### 5.11 Uji otomatis berlapis
e2e via klien WebSocket, UI via Firefox headless + mic palsu, kalibrasi retriever — semuanya juga menghasilkan folder `results/`.

### 5.12 Aturan kerja aman di mesin bersama
Tes server di port lain, cek `ss -ltnp`, hentikan hanya PID sendiri, **jangan `pkill -f`** — penting karena PC lab dipakai bersama.

---

## 6. Rekomendasi Penerapan untuk TA Rendy

Kondisi `TA Rendy` saat ini: `AGENT.md` (kosong), `plan_revision.md`, folder `data/`, `docs/`, `src/` (kosong).
Karena fokus Rendy = **gateway, orkestrator, UI kiosk, lifecycle model GPU**, struktur yang disarankan:

```
TA Rendy/
├── CLAUDE.md / AGENT.md     # konteks proyek, protokol kerja, konvensi (isi AGENT.md yang masih kosong)
├── run.py                   # menu: benchmark strategi A–D, uji transisi mode, uji stabilitas 8 jam, gateway
├── requirements.txt         # versi di-pin
├── configs/
│   ├── registry.yaml        # ID model, endpoint/port, kebutuhan VRAM, mode, eksklusif, dependensi, load/unload
│   ├── modes.yaml           # matriks mode kiosk (percakapan, busana, try-on, photobooth)
│   └── benchmark.yaml       # strategi A–D, workload, jumlah giliran, interval sampling NVML
├── docs/
│   ├── CHECKPOINT.md  DECISIONS.md  EXPERIMENT_LOG.md  METRICS.md  RUNBOOK.md
│   ├── RESEARCH_ROADMAP.md  # M0–M4 dari plan_revision.md + mapping ke bab
│   ├── API_CONTRACT.md      # kontrak /health /load /unload /infer /metrics (padanan PIPELINE.md Ferdie)
│   ├── SERVICES.md          # inventaris layanan 6 TA (pemilik, model, VRAM terukur, runtime)
│   └── WRITING_BRIEF.md
├── src/
│   ├── gateway/             # FastAPI REST + WebSocket
│   ├── orchestrator/        # registry, lifecycle, kebijakan mode, strategi A–D
│   ├── monitor/             # NVML sampler (50–100 ms), metrik
│   ├── services/            # adapter/stub tiap layanan (stt_llm_tts, avatar, busana, tryon, photobooth)
│   └── ui/                  # web potret untuk Chromium kiosk
├── experiments/
│   ├── runlog.py            # tiru langsung dari Ferdie
│   ├── m0_hardware/  m1_voice_baseline/  m2_strategi/  m3_transisi/  m4_stabilitas/
├── data/                    # workload uji (rekaman ID/EN, skenario transisi) + README
└── results/                 # <ts>_<jenis>_<tag>/ + README
```

**Prioritas yang disarankan:**
1. Salin **pola** `runlog.py` (meta.json + SHA-256 + run.log) — sangat cocok untuk metrik VRAM/load/unload/swap.
   Perbaiki kelemahan yang Ferdie catat sendiri: tulis `meta.json` **di awal** run (status `running`), bukan hanya di akhir.
2. Buat `CHECKPOINT.md`, `DECISIONS.md`, `EXPERIMENT_LOG.md` (dengan status ✅/⚠️/❌) sejak hari pertama.
3. Jadikan `configs/registry.yaml` satu-satunya sumber kebenaran registry (seperti `AGENT.md` bagi Ferdie).
4. Buat `METRICS.md` untuk definisi operasional: VRAM puncak, waktu load/unload/swap, "kebocoran VRAM", keberhasilan.
5. Manfaatkan hasil Ferdie sebagai **data awal layanan suara**: VRAM gabungan 6,6 GB (EXP-065), STT int8 1,1 GB (EXP-066),
   latensi audio pertama 1,49 s (EXP-067), protokol WebSocket di `docs/PIPELINE.md` §2 → bahan kontrak API & budget VRAM.
   Sebutkan sumbernya (EXP-xxx) bila dikutip.

> [!NOTE]
> Tidak perlu meniru semuanya. Bagian yang terlalu khusus pipeline suara (normalisasi ejaan WER, rubrik LLM,
> prosodi TTS, knowledge base) tidak relevan untuk orkestrator — yang ditiru adalah **disiplin pencatatan,
> konfigurasi, modularitas, dan dokumentasi**.

---

## 7. Hal yang Perlu Diwaspadai (pelajaran dari log Ferdie)

- **GPU Xid 79** muncul saat beban penuh berkelanjutan (88–91 °C, 145 W) → uji stabilitas 8 jam Rendy wajib memonitor suhu/daya; pertimbangkan `nvidia-smi -pl`.
- **Pengukuran VRAM bisa tercemar** oleh proses lain/konteks CUDA → ukur dari luar proses via NVML, catat proses lain yang berjalan.
- **Ollama `keep_alive`** membuat model tetap di VRAM antargiliran → relevan untuk strategi load/unload.
- **Versi runtime berubah diam-diam** (Ollama 0.14 → 0.40 di-upgrade pihak lain) → selalu catat versi di `meta.json`.
- Port 8000 dipakai pipeline Ferdie → sepakati alokasi port antarlayanan di registry.
