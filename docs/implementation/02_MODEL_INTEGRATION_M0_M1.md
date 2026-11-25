# 02_MODEL_INTEGRATION_M0_M1.md — Uji Mandiri Model & Kontrak Adapter Layanan AI

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Milestone M0 (Uji Mandiri) & M1 (Pipeline Suara Lokal)  
> **Target:** Model Percakapan (STT, LLM, TTS) & Adapter Seragam

---

## 1. Tujuan Dokumen
1. Menentukan kandidat model AI open-weight yang efisien dan kompatibel dengan GPU NVIDIA RTX 5060 8 GB.
2. Melakukan pengujian mandiri (*standalone benchmark*) untuk mencatat data baseline: VRAM puncak ($V_{\text{peak}}$), waktu pemuatan ($T_{\text{load}}$), dan waktu inferensi ($T_{\text{infer}}$).
3. Mendefinisikan **Kontrak Adapter Seragam (Uniform Service Contract)** agar model apa pun dapat dikendalikan oleh Orchestrator dengan protokol yang identik.

---

## 2. Kandidat Model AI & Profil Baseline Estimasi

| Domain / Fungsi | Model Rekomendasi | Runtime / Engine | Estimasi Bobot | Estimasi VRAM Aktif | Peran Kiosk |
|---|---|---|---|---|---|
| **STT** (Speech-to-Text) | Faster-Whisper (small / medium) | CTranslate2 + cuDNN | ~500 MB – 1.5 GB | ~1.0 – 1.8 GB | Konversi suara pengguna ke teks |
| **LLM** (Penalaran Lokal) | Qwen 2.5 7B / Llama 3.2 3B (Q4_K_M) | llama.cpp server / Ollama | ~2.2 – 4.5 GB | ~3.0 – 5.2 GB | Pemrosesan dialog & perintah |
| **TTS** (Text-to-Speech) | Piper TTS (id_ID / en_US) | ONNX Runtime / PyTorch | ~100 – 300 MB | ~0.5 – 1.0 GB (atau CPU) | Sintesis suara asisten kios |
| **Visual / Try-On** | IDM-VTON / CatVTON (Exclusive) | PyTorch + Diffusers | ~4 – 6 GB | ~6.5 – 7.8 GB | Fitting busana virtual |
| **Photobooth** | SDXL Turbo / Realistic Vision | Diffusers / ComfyUI engine | ~3.5 – 5 GB | ~6.0 – 7.5 GB | Foto kreasi & filter cerdas |

---

## 3. Kontrak Adapter Seragam (Uniform Microservice Contract)

Setiap layanan AI wajib diekspos sebagai HTTP microservice lokal independen (baik berjalan sebagai proses mandiri atau di dalam kontainer Docker). Orchestrator berkomunikasi menggunakan kontrak API standar berikut:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIFORM SERVICE ADAPTER CONTRACT                     │
├─────────────────┬──────────┬───────────────────────────────────────────┤
│ Endpoint        │ Method   │ Deskripsi & Perilaku                      │
├─────────────────┼──────────┼───────────────────────────────────────────┤
│ /health         │ GET      │ Mengembalikan { "status": "UP",           │
│                 │          │   "model_loaded": bool, "vram_mb": float }│
│ /load           │ POST     │ Memuat bobot model ke VRAM GPU.           │
│                 │          │ Mengembalikan HTTP 200 setelah READY.    │
│ /unload         │ POST     │ Melepaskan alokasi VRAM & membersihkan   │
│                 │          │ cache CUDA (torch.cuda.empty_cache()).    │
│ /infer          │ POST     │ Menerima payload input (audio/teks/gambar)│
│                 │          │ dan mengembalikan hasil komputasi AI.     │
└─────────────────┴──────────┴───────────────────────────────────────────┘
```

### Contoh Kode Adapter Python (FastAPI Wrapper Template):
Simpan templat ini di `src/services_adapters/base_adapter.py`:

```python
import gc
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Uniform AI Service Adapter")

class ModelWrapper:
    def __init__(self):
        self.model = None
        self.is_loaded = False

    def load(self):
        if not self.is_loaded:
            # Contoh pemanggilan model PyTorch/CTranslate2
            # self.model = AutoModel.from_pretrained(...)
            self.is_loaded = True

    def unload(self):
        if self.is_loaded:
            del self.model
            self.model = None
            self.is_loaded = False
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

model_instance = ModelWrapper()

@app.get("/health")
def health():
    return {
        "status": "UP",
        "model_loaded": model_instance.is_loaded,
        "vram_allocated_mb": torch.cuda.memory_allocated() / (1024**2) if torch.cuda.is_available() else 0
    }

@app.post("/load")
def load_model():
    model_instance.load()
    return {"status": "READY", "message": "Model loaded into VRAM"}

@app.post("/unload")
def unload_model():
    model_instance.unload()
    return {"status": "STOPPED", "message": "VRAM released"}

@app.post("/infer")
def infer(payload: dict):
    if not model_instance.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded. Call /load first.")
    # Logika inferensi murni ...
    return {"result": "sample_output"}
```

---

## 4. Prosedur Uji Mandiri Model (Standalone Benchmark Script)

Sebelum diintegrasikan ke Orchestrator, jalankan skrip pengujian mandiri untuk setiap model guna merekam $V_{\text{peak}}$, $T_{\text{load}}$, dan $T_{\text{infer}}$:

```bash
# Contoh pengujian mandiri STT Faster-Whisper
python -c "
import time, pynvml
from faster_whisper import WhisperModel

pynvml.nvmlInit()
h = pynvml.nvmlDeviceGetHandleByIndex(0)
v0 = pynvml.nvmlDeviceGetMemoryInfo(h).used / 1024**2

t0 = time.perf_counter()
model = WhisperModel('small', device='cuda', compute_type='float16')
t_load = time.perf_counter() - t0

v1 = pynvml.nvmlDeviceGetMemoryInfo(h).used / 1024**2
print(f'STT Loaded in {t_load:.3f} s | VRAM Added: {v1 - v0:.1f} MB')
"
```

---

## 5. Pipeline Suara Terpadu (Milestone M1)

Untuk menguji alur beruntun STT $\rightarrow$ LLM $\rightarrow$ TTS:
1. Rekam sampel audio masukan pertanyaan standar (misal: "Halo, apa saja layanan yang tersedia di kios ini?").
2. Ukur jeda waktu per tahap:
   - $T_{\text{STT}}$: Waktu transkripsi audio ke teks.
   - $T_{\text{LLM-TTFT}}$: Waktu pemrosesan token pertama LLM.
   - $T_{\text{TTS}}$: Waktu sintesis audio respons.
   - $T_{\text{e2e}}$: Total waktu dari akhir audio pengguna hingga audio jawaban pertama siap diputar.
3. Verifikasi apakah ketiga model dapat resident bersamaan atau memerlukan pelepasan memori jika VRAM mendekati 7.5 GB.

---

## 6. Kriteria Keberhasilan Milestone M0 & M1
- [ ] Masing-masing model (STT, LLM, TTS) sukses dieksekusi secara mandiri pada GPU lokal.
- [ ] VRAM puncak dan waktu pemuatan baseline tercatat rapi di `configs/services.yaml`.
- [ ] Layanan mengekspos endpoint `/health`, `/load`, `/unload`, dan `/infer` yang merespons dengan benar.
