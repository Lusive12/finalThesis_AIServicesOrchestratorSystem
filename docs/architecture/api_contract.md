# api_contract.md — Kontrak Antarmuka Layanan AI (Microservices API Contract)

> **Lokasi:** `docs/architecture/api_contract.md`  
> **Fungsi:** Spesifikasi kontrak API seragam yang wajib diimplementasikan oleh setiap adapter model AI (STT, LLM, TTS, Visual) agar dapat dikelola secara modular oleh Orchestrator.  
> **Kapan AI membaca:** Saat mengimplementasikan adapter model baru atau menyambungkan service ke Orchestrator.

---

## 1. Prinsip Kontrak Seragam (Uniform Service Contract)

Setiap layanan AI lokal—baik yang berjalan sebagai proses independen maupun kontainer Docker—wajib mengekspos 5 endpoint standar HTTP:

```text
GET  /health      -> Memeriksa status proses dan kesiapan memori
POST /load        -> Memuat bobot model ke dalam VRAM GPU
POST /unload      -> Melepaskan model dari VRAM GPU
POST /infer       -> Menjalankan inferensi data masukan
GET  /metrics     -> Melaporkan telemetri latensi dan konsumsi memori internal
```

---

## 2. Rincian Spesifikasi Endpoint

### 2.1 `GET /health`
Mengembalikan status siklus hidup model dan lokasi bobot saat ini.
- **Response Format (`application/json`):**
```json
{
  "service_id": "speech_llm",
  "status": "READY",
  "memory_state": "IN_VRAM",
  "vram_allocated_mb": 3520.5,
  "uptime_seconds": 124.8
}
```
*Nilai status yang valid: `STOPPED`, `STARTING`, `READY`, `BUSY`, `STOPPING`, `ERROR`.*  
*Nilai memory_state: `UNLOADED`, `IN_HOST_RAM`, `IN_VRAM`.*

### 2.2 `POST /load`
Memerintahkan adapter memuat model ke GPU.
- **Request Body:**
```json
{
  "strategy": "PINNED_SWAP",
  "keep_in_host_ram": true
}
```
- **Response:** HTTP 200 dengan durasi pemuatan (`load_duration_ms`).

### 2.3 `POST /unload`
Memerintahkan pelepasan model dari VRAM GPU.
- **Request Body:**
```json
{
  "keep_in_host_ram": true,
  "force_cleanup": true
}
```
- **Response:** HTTP 200 setelah alokasi VRAM dilepas (`vram_freed_mb`).

### 2.4 `POST /infer`
Menerima payload input inferensi dan mengembalikan hasil pemrosesan.
- **Request Body (Contoh Speech LLM):**
```json
{
  "request_id": "req-turn-042",
  "prompt": "Di mana lokasi ruang dosen departemen?",
  "stream": false
}
```
- **Response:** HTTP 200 dengan hasil inferensi dan durasi komputasi murni (`infer_duration_ms`).

### 2.5 `GET /metrics`
Mengembalikan metrik internal model:
```json
{
  "last_infer_duration_ms": 420.5,
  "time_to_first_token_ms": 185.2,
  "peak_vram_mb": 3610.0,
  "total_requests_served": 42
}
```
