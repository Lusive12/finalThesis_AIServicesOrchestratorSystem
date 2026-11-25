# 📐 Proposal Restrukturisasi Proyek TA Smart Kiosk

> **Tujuan:** Membuat struktur proyek yang bersih, modular, dan AI-credit-efficient — setiap `.md` punya scope jelas sehingga AI agent hanya perlu membaca file yang relevan, bukan seluruh repo.

---

## 1. Diagnosis Masalah Struktur Saat Ini

### ❌ Masalah yang ditemukan

| # | Masalah | Contoh |
|---|---|---|
| 1 | **File root terlalu banyak & overlapping** | `implement.md` hanya redirect ke `implementation.md`. `PPT.md` campur dengan docs kode. `writing.md` di root padahal mestinya di `docs/`. |
| 2 | **AGENT.md terlalu besar (466 baris, 36KB)** | Mencampur: protokol AI agent, arsitektur sistem, strategi GPU, metrik, pedoman penulisan, checklist — AI harus baca semua walau hanya butuh 1 topik. |
| 3 | **Docs tidak terkelompok fungsi** | Semua flat di `docs/`: file bab 3 LaTeX, checkpoint, metrik, diagram, analisis referensi — semuanya sejajar tanpa hirarki. |
| 4 | **Belum ada `src/` yang terisi** | Folder code belum ada; `scripts/` berisi campuran utility dan diagram renderer. |
| 5 | **Belum ada `configs/` terpisah** | Konfigurasi (services.yaml, benchmark.yaml) belum ada sebagai folder sendiri. |
| 6 | **Belum ada `results/` dan `experiments/`** | Belum ada tempat standar untuk output benchmark. |
| 7 | **File `planning/` dan `given_materials/` campur** | Material dosen dan planning ada di root project. |
| 8 | **Redundansi konten tinggi** | `ARSITEKTUR_UMUM.md`, `DIAGRAM_METODOLOGI_BAB3.md`, `PERANCANGAN_SISTEM_BAB3.tex`, `METODOLOGI_PENELITIAN_BAB3.md` banyak overlap deskripsi yang sama. |

---

## 2. Struktur Baru yang Diusulkan

```
proof-concept-smartkiosk/
│
├── AGENT.md                    # [DIPERKECIL] Hanya: identitas proyek, protokol memulai sesi,
│                               #   daftar file & fungsinya, guardrail AI. Max ~150 baris.
│                               #   Menjadi "peta navigasi" — bukan ensiklopedia.
│
├── run.py                      # Satu pintu eksekusi: `python run.py <aksi>`
├── requirements.txt            # Dependensi Python (versi di-pin)
├── .gitignore
│
├── configs/                    # ═══ KONFIGURASI (YAML) ═══
│   ├── services.yaml           # Registry layanan: ID, endpoint, VRAM, mode, eksklusif
│   ├── modes.yaml              # Matriks mode kiosk (percakapan, busana, try-on, photobooth)
│   └── benchmark.yaml          # Parameter benchmark: strategi A-D, workload, sampling NVML
│
├── docs/                       # ═══ DOKUMENTASI PROYEK (GROUPED BY FUNCTION) ═══
│   │
│   ├── checkpoint.md           # Tracking tugas aktif, progres, langkah berikutnya
│   ├── decisions.md            # Log keputusan teknis (ADR-xxx) → bahan Bab 3
│   ├── metrics.md              # 5 metrik evaluasi: definisi, rumus, target, cara ukur
│   ├── evaluation_plan.md      # Rencana evaluasi, milestone, timeline → bahan Bab 4
│   ├── research_roadmap.md     # Roadmap M0-M4, mapping fase ke bab laporan
│   ├── pipeline.md             # Workflow & pipeline setiap tugas besar
│   ├── tech_stack.md           # Hardware & software: spesifikasi, versi, pemetaan TB
│   ├── runbook.md              # Panduan manual: cara jalankan sistem, troubleshoot
│   ├── guardrail.md            # Batasan AI agent: apa yang boleh/tidak boleh dilakukan
│   │
│   ├── writing/                # --- Sub-folder: Penulisan Laporan ---
│   │   ├── writing_guide.md    # Pedoman bahasa, sitasi IEEE, gaya paragraf
│   │   ├── diagram_guide.md    # Standar visual diagram, ekspor PNG, template
│   │   └── ppt_guide.md        # Struktur dan bahan slide presentasi seminar
│   │
│   ├── architecture/           # --- Sub-folder: Arsitektur & Perancangan ---
│   │   ├── architecture_overview.md  # Arsitektur umum sistem (formal + mudah)
│   │   ├── strategy_comparison.md    # 4 strategi GPU: flowchart & perbandingan
│   │   └── api_contract.md           # Kontrak API: /health, /load, /unload, /infer
│   │
│   ├── implementation/         # --- Sub-folder: Panduan Implementasi Step-by-Step ---
│   │   ├── 00_setup_env.md
│   │   ├── 01_hardware_audit.md
│   │   ├── 02_model_integration.md
│   │   ├── 03_orchestrator_core.md
│   │   ├── 04_resource_management.md
│   │   ├── 05_exclusive_mode.md
│   │   ├── 06_kiosk_ui.md
│   │   └── 07_benchmark_evaluation.md
│   │
│   ├── bab3_latex/             # --- Sub-folder: Naskah LaTeX Bab 3 ---
│   │   ├── metodologi_penelitian.tex
│   │   ├── perancangan_sistem.tex
│   │   ├── bahan_peralatan.tex
│   │   ├── metrics_formulas.tex
│   │   └── references.bib
│   │
│   └── references/             # --- Sub-folder: Material Referensi ---
│       ├── analisis_ferdie.md        # Analisis struktur TA Ferdie
│       ├── rencana_revisi_bab.md     # Draf revisi Bab I-III
│       └── extracted_materials/      # PDF → MD conversions + images
│           ├── images/
│           ├── draft_rendy.md
│           ├── paper_adaptive_gpu.md
│           └── README.md
│
├── src/                        # ═══ SOURCE CODE (3 TUGAS BESAR) ═══
│   │
│   ├── kiosk_ui/               # --- TB1: UI/UX Chromium Kiosk ---
│   │   ├── index.html          # Halaman utama portrait 9:16
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── app.js          # Logic utama UI
│   │   │   ├── websocket.js    # Koneksi WebSocket ke orchestrator
│   │   │   └── mode_manager.js # Perpindahan tampilan mode
│   │   └── assets/             # Ikon, gambar UI
│   │
│   ├── orchestrator/           # --- TB2: AI Service Orchestrator ---
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── gateway.py          # REST + WebSocket gateway
│   │   ├── registry.py         # Service registry (baca services.yaml)
│   │   ├── lifecycle.py        # State machine: STOPPED→STARTING→READY→STOPPING→ERROR
│   │   ├── mode_controller.py  # Kebijakan mode & transisi
│   │   ├── request_router.py   # Routing request ke service yang tepat
│   │   └── models.py           # Pydantic schemas
│   │
│   └── resource_mgmt/          # --- TB3: Resource Management ---
│       ├── __init__.py
│       ├── gpu_monitor.py      # PyNVML sampler (50-100ms)
│       ├── strategy_base.py    # Abstract base class strategi
│       ├── strategy_a_resident.py    # All-Resident
│       ├── strategy_b_naive.py       # Naive Load/Unload
│       ├── strategy_c_pinned.py      # Pinned-Memory Swap
│       ├── strategy_d_prefetch.py    # Prefetch
│       ├── vram_barrier.py     # Exclusive GPU mode barrier
│       └── metrics_logger.py   # Pencatat 5 metrik ke CSV/JSONL
│
├── experiments/                # ═══ SKRIP EKSPERIMEN ═══
│   ├── runlog.py               # Pencatat run otomatis (meta.json + SHA-256)
│   ├── run_benchmark.py        # Runner benchmark utama
│   ├── calculate_stats.py      # Kalkulator statistik deskriptif
│   └── workloads/              # Data input uji (audio, gambar, skenario)
│       └── README.md
│
├── results/                    # ═══ HASIL RUNNING ═══
│   └── README.md               # Konvensi penamaan: <YYYYMMDD_HHMMSS>_<jenis>_<tag>/
│
├── assets/                     # ═══ ASET VISUAL ═══
│   └── diagrams/               # PNG diagram resolusi tinggi untuk laporan
│       ├── bab3_01_arsitektur_umum.png
│       ├── bab3_02_alur_pengguna_ui.png
│       ├── bab3_03_alur_kerja_orchestrator.png
│       ├── bab3_04_alur_kerja_resource_management.png
│       ├── bab3_05_tahapan_penelitian.png
│       └── strategi_*.png
│
├── scripts/                    # ═══ UTILITY SCRIPTS ═══
│   ├── launch_kiosk.sh         # Chromium kiosk launcher
│   ├── convert_pdf_to_md.py    # PDF to Markdown converter
│   └── render_diagram.py       # Mermaid → PNG renderer
│
└── given_materials/            # ═══ MATERIAL DARI DOSEN/TIM (READ-ONLY) ═══
    ├── PROOF_OF_CONCEPT.md
    ├── pc-spec.txt
    ├── gambar/
    └── ...
```

---

## 3. Mapping: File Lama → File Baru

| File Lama (Sekarang) | Pindah Ke | Aksi |
|---|---|---|
| `AGENT.md` (466 baris) | `AGENT.md` (diperkecil ~150 baris) | **Rewrite** — hanya jadi peta navigasi + guardrail. Konten dipecah ke docs/ |
| `implement.md` | *(hapus)* | Redirect file, sudah tidak perlu |
| `implementation.md` | Konten masuk ke `docs/research_roadmap.md` + `docs/runbook.md` | **Split & merge** |
| `writing.md` | `docs/writing/writing_guide.md` + `docs/writing/diagram_guide.md` | **Split** |
| `PPT.md` | `docs/writing/ppt_guide.md` | **Move** |
| `docs/CHECKPOINT.md` | `docs/checkpoint.md` | **Rename** (lowercase) |
| `docs/DECISIONS.md` | `docs/decisions.md` | **Rename** |
| `docs/METRICS.md` | `docs/metrics.md` | **Rename** |
| `docs/TECH_STACK.md` | `docs/tech_stack.md` | **Rename** |
| `docs/ARSITEKTUR_UMUM.md` | `docs/architecture/architecture_overview.md` | **Move** |
| `docs/DIAGRAM_STRATEGI_PENGELOLAAN_MODEL.md` | `docs/architecture/strategy_comparison.md` | **Move** |
| `docs/DIAGRAM_METODOLOGI_BAB3.md` | `docs/architecture/architecture_overview.md` (merge) | **Merge** |
| `docs/METODOLOGI_PENELITIAN_BAB3.md` | `docs/bab3_latex/metodologi_penelitian.tex` area | **Move** |
| `docs/PERANCANGAN_SISTEM_BAB3.tex` | `docs/bab3_latex/perancangan_sistem.tex` | **Move** |
| `docs/BAHAN_DAN_PERALATAN_BAB3.tex` | `docs/bab3_latex/bahan_peralatan.tex` | **Move** |
| `docs/METRICS_LATEX_BAB3.tex` | `docs/bab3_latex/metrics_formulas.tex` | **Move** |
| `docs/references.bib` | `docs/bab3_latex/references.bib` | **Move** |
| `docs/ANALISIS_STRUKTUR_TA_FERDIE.md` | `docs/references/analisis_ferdie.md` | **Move** |
| `docs/tempSOURCES.md` | `docs/references/` atau hapus | **Move/cleanup** |
| `docs/extracted_materials/` | `docs/references/extracted_materials/` | **Move** |
| `docs/implementation/*.md` | `docs/implementation/*.md` | **Keep** (rename lowercase) |
| `planning/Rencana_TA_dan_Revisi_Bab_I-III.md` | `docs/references/rencana_revisi_bab.md` | **Move** |
| `planning/bimbingan TA kedua...txt` | `docs/references/` | **Move** |
| `scripts/*.py` | `scripts/` (keep utility), diagram renders stay | **Cleanup** |

---

## 4. Spesifikasi & Fungsi Setiap File docs/

### 📌 Root Level docs/

| File | Scope & Fungsi | Kapan AI Baca | Ukuran Target |
|---|---|---|---|
| `checkpoint.md` | **Status kerja aktif.** Tugas yang sedang jalan, checklist per milestone (M0-M4), blocker, file yang disentuh, langkah berikutnya. | Setiap memulai sesi kerja baru | ~100-200 baris |
| `decisions.md` | **Log keputusan teknis.** Format ADR-xxx: konteks, opsi, keputusan, alasan, konsekuensi. Bahan langsung Bab 3. | Saat membuat keputusan arsitektur/teknis | Tumbuh organik |
| `metrics.md` | **Definisi 5 metrik evaluasi.** Rumus matematis, cara ukur (PyNVML, perf_counter), target PoC, titik sampling. | Saat implementasi benchmark/evaluasi | ~200 baris |
| `evaluation_plan.md` | **Rencana evaluasi & milestone.** Timeline pengerjaan, mapping ke Bab 4, kriteria lulus tiap tahap PoC. | Saat planning atau menyusun Bab 4 | ~150 baris |
| `research_roadmap.md` | **Peta jalan riset M0-M4.** Fase, keluaran, kriteria lulus, prioritas kerja, mapping ke bab laporan. | Saat perlu tahu big picture | ~200 baris |
| `pipeline.md` | **Workflow setiap tugas besar.** Alur data TB1→TB2→TB3, sequence komunikasi, format request/response. | Saat implementasi atau debug alur | ~150 baris |
| `tech_stack.md` | **Inventaris hardware & software.** Spesifikasi, versi, pemetaan ke 3 tugas besar. | Saat setup environment atau tulis Bab 3.2 | ~100 baris |
| `runbook.md` | **Panduan operasional.** Step-by-step menjalankan sistem, benchmark, kiosk. Troubleshooting. | Saat perlu jalankan/debug sistem | ~150 baris |
| `guardrail.md` | **Batasan AI agent.** Apa yang boleh/tidak boleh AI lakukan, scope, limitasi, aturan keamanan. | Dibaca oleh AI agent tiap sesi | ~80 baris |

### 📂 docs/writing/

| File | Scope | Kapan AI Baca |
|---|---|---|
| `writing_guide.md` | Pedoman bahasa Indonesia ilmiah, pola paragraf, sitasi IEEE, integritas referensi | Saat menulis/mengedit laporan |
| `diagram_guide.md` | Standar visual diagram, warna, font, ekspor PNG 300 DPI, template Mermaid | Saat membuat diagram baru |
| `ppt_guide.md` | Struktur slide presentasi, konten per slide | Saat mempersiapkan presentasi |

### 📂 docs/architecture/

| File | Scope | Kapan AI Baca |
|---|---|---|
| `architecture_overview.md` | Arsitektur umum end-to-end, 6 modul, penjelasan formal & analogi | Saat perlu memahami desain keseluruhan |
| `strategy_comparison.md` | 4 strategi GPU: penjelasan, flowchart Mermaid, tabel perbandingan | Saat implementasi strategi atau tulis Bab 3 |
| `api_contract.md` | Kontrak endpoint: /health, /load, /unload, /infer, /metrics. Format, status code | Saat implementasi gateway/adapter |

### 📂 docs/implementation/

Tetap seperti sekarang (sudah bagus), hanya di-rename lowercase. Setiap file = 1 milestone step.

### 📂 docs/bab3_latex/

Semua naskah LaTeX dan .bib untuk Bab 3. AI hanya masuk sini saat mode penulisan.

### 📂 docs/references/

Material referensi read-only: analisis TA teman, draf revisi bab lama, extracted PDF.

---

## 5. Desain AGENT.md yang Baru (~150 baris)

AGENT.md baru hanya berisi:
1. **Identitas proyek** (5 baris: judul, pemilik, departemen)
2. **Peta navigasi file** — tabel "mau ngapain → baca file ini"
3. **Protokol memulai sesi** (10 baris: baca checkpoint dulu, cek git status)
4. **Guardrail ringkas** → pointer ke `docs/guardrail.md` untuk detail
5. **Prioritas kerja saat ini** → pointer ke `docs/checkpoint.md`

Konten besar yang saat ini di AGENT.md dipecah ke:
- §2 Kondisi Hardware → `docs/tech_stack.md`
- §3 Arsitektur → `docs/architecture/architecture_overview.md`
- §4 Domain Fitur → `docs/pipeline.md`
- §5 Tahapan PoC → `docs/research_roadmap.md`
- §6 Strategi GPU → `docs/architecture/strategy_comparison.md`
- §7 Metrik → `docs/metrics.md`
- §8 Protokol Eksperimen → `docs/runbook.md` + `docs/evaluation_plan.md`
- §9 Pedoman Kode → `docs/guardrail.md`
- §10 Pedoman Penulisan → `docs/writing/writing_guide.md`
- §11-12 Fakta/Target/Larangan → `docs/guardrail.md`
- §13 Dokumen Proyek → tabel navigasi di AGENT.md baru
- §14 Prioritas → `docs/checkpoint.md`

---

## 6. Keuntungan Struktur Baru

| Aspek | Sebelum | Sesudah |
|---|---|---|
| **AI credit efficiency** | AI harus baca AGENT.md 36KB + semua docs flat | AI baca AGENT.md 5KB (peta) → langsung ke file spesifik |
| **Context precision** | Mau implementasi strategi GPU? Baca AGENT.md 466 baris | Baca `docs/architecture/strategy_comparison.md` saja |
| **Separation of concerns** | Docs campur: LaTeX, checkpoint, arsitektur, referensi | Grouped: writing/, architecture/, implementation/, bab3_latex/, references/ |
| **Code structure** | `src/` kosong | `src/kiosk_ui/`, `src/orchestrator/`, `src/resource_mgmt/` |
| **Scalability** | Tambah doc = makin flat & kacau | Tambah doc = masuk sub-folder yang tepat |
| **Onboarding** | Baca AGENT.md 36KB untuk mulai | Baca AGENT.md 5KB → lihat tabel → langsung ke file yang relevan |

---

## 7. Pertanyaan Sebelum Eksekusi

Sebelum saya mulai memindahkan dan menulis ulang file, saya perlu konfirmasi:

> [!IMPORTANT]
> 1. **Apakah kamu setuju dengan struktur folder `src/` yang dibagi 3?** (`kiosk_ui/`, `orchestrator/`, `resource_mgmt/`)
> 2. **Apakah `planning/` boleh di-merge ke `docs/references/`?** Atau kamu mau simpan terpisah?
> 3. **Apakah file LaTeX Bab 3 perlu sub-folder sendiri (`docs/bab3_latex/`)?** Atau kamu mau taruh flat di `docs/`?
> 4. **Apakah `given_materials/` tetap di root?** (saya rekomendasikan tetap — ini read-only dari dosen)
> 5. **Mau langsung eksekusi restructuring, atau mau review/adjust proposal ini dulu?**
