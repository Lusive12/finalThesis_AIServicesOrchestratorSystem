# 04_RESOURCE_MANAGEMENT_M2.md — Manajemen Sumber Daya & Implementasi 4 Strategi Memori GPU

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Milestone M2 (Tugas Besar 3: Resource Management)  
> **Target:** 4 Strategi Pengelolaan GPU, PyNVML Background Sampler, Logging Metrik Evaluasi

---

## 1. Tujuan Dokumen
1. Mengimplementasikan logika eksekusi **empat strategi pengelolaan siklus hidup model** pada GPU lokal:
   - **(a) All-Resident**
   - **(b) Naive Load/Unload**
   - **(c) Pinned-Memory Swap**
   - **(d) Prefetch**
2. Membangun modul *background sampler* berbasis PyNVML yang mencuplik penggunaan VRAM fisik dan utilisasi GPU setiap 50–100 ms tanpa membebani latensi inferensi.
3. Mencatat 5 pilar metrik evaluasi resmi sesuai [METRICS.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/docs/METRICS.md).

---

## 2. Arsitektur & Logika 4 Strategi Pengelolaan GPU

| ID | Strategi | Perilaku Pembebanan Memori | Rantai Aksi Transisi | Kasus Penggunaan Ideal |
|---|---|---|---|---|
| **(a)** | **All-Resident** | Seluruh model tetap dimuat di VRAM ($\le 7,5\text{ GB}$) | Permintaan masuk $\rightarrow$ langsung inferensi (tanpa swap) | Model ringkas / terkuantisasi intensif |
| **(b)** | **Naive Load/Unload** | Model di-load dari NVMe SSD saat butuh, di-unload setelah selesai | Baca Disk $\rightarrow$ Alokasi VRAM $\rightarrow$ Inferensi $\rightarrow$ Pelepasan VRAM | Layanan jarang dipakai / memori sangat ketat |
| **(c)** | **Pinned-Memory Swap** | Bobot model siaga di Host RAM (*pinned memory*), disalin via PCIe | Salin Host-to-Device (PCIe) $\rightarrow$ Inferensi $\rightarrow$ Pelepasan VRAM | Alternatif lebih cepat dari pembacaan disk |
| **(d)** | **Prefetch** | Model berikutnya dimuat di latar belakang saat model aktif inferensi | Background async load model $N+1$ $\rightarrow$ Handover instan | Skenario alur percakapan terprediksi |

---

## 3. Implementasi Pemantau VRAM PyNVML (Continuous Sampler)

Simpan modul ini di `src/resource_manager/gpu_monitor.py`:

```python
import time
import threading
import pynvml

class GPUMonitor:
    def __init__(self, device_index=0, sampling_interval_ms=50):
        self.device_index = device_index
        self.interval = sampling_interval_ms / 1000.0
        self.is_running = False
        self.thread = None
        
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
        
        self.peak_vram_mb = 0.0
        self.samples = []

    def _sample_loop(self):
        while self.is_running:
            try:
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
                used_mb = mem_info.used / (1024 ** 2)
                
                util = pynvml.nvmlDeviceGetUtilizationRates(self.handle)
                gpu_util = util.gpu
                
                t_now = time.perf_counter()
                
                if used_mb > self.peak_vram_mb:
                    self.peak_vram_mb = used_mb
                    
                self.samples.append({
                    "timestamp": t_now,
                    "vram_used_mb": used_mb,
                    "gpu_util_percent": gpu_util
                })
            except Exception as e:
                pass
            time.sleep(self.interval)

    def start(self):
        self.is_running = True
        self.peak_vram_mb = 0.0
        self.samples = []
        self.thread = threading.Thread(target=self._sample_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        return {
            "peak_vram_mb": self.peak_vram_mb,
            "sample_count": len(self.samples),
            "samples": self.samples
        }

    def close(self):
        self.stop()
        try:
            pynvml.nvmlShutdown()
        except Exception:
            pass
```

---

## 4. Implementasi Dispatcher Strategi Model

Simpan modul ini di `src/resource_manager/strategy_executor.py`:

```python
import time
import httpx
from src.resource_manager.gpu_monitor import GPUMonitor

class StrategyExecutor:
    def __init__(self, services_config):
        self.services = services_config
        self.monitor = GPUMonitor(device_index=0, sampling_interval_ms=50)

    async def execute_turn(self, strategy_type: str, active_service_id: str, payload: dict):
        """
        Mengeksekusi satu siklus interaksi dan merekam 5 pilar metrik:
        - T_e2e (Total Latency)
        - T_swap (Waktu transisi/swap)
        - T_infer (Waktu komputasi inferensi)
        - V_peak (VRAM Puncak)
        - Success/Status
        """
        metrics = {
            "strategy": strategy_type,
            "service_id": active_service_id,
            "t_swap_sec": 0.0,
            "t_infer_sec": 0.0,
            "t_e2e_sec": 0.0,
            "v_peak_mb": 0.0,
            "success": False
        }

        self.monitor.start()
        t_start_e2e = time.perf_counter()
        target = self.services[active_service_id]

        try:
            # --- TAHAP 1: SWAP & READINESS ---
            t_start_swap = time.perf_counter()
            
            if strategy_type == "ALL_RESIDENT":
                # Model diasumsikan sudah ready di VRAM
                metrics["t_swap_sec"] = 0.0
                
            elif strategy_type == "NAIVE_LOAD_UNLOAD":
                # Muat dari SSD ke GPU
                async with httpx.AsyncClient() as client:
                    await client.post(f"{target['endpoint']}{target['load_path']}", timeout=30.0)
                metrics["t_swap_sec"] = time.perf_counter() - t_start_swap
                
            elif strategy_type == "PINNED_SWAP":
                # Salin bobot dari Host RAM Pinned Memory via PCIe
                async with httpx.AsyncClient() as client:
                    await client.post(f"{target['endpoint']}/swap_in", timeout=30.0)
                metrics["t_swap_sec"] = time.perf_counter() - t_start_swap
                
            elif strategy_type == "PREFETCH":
                # Pada prefetch, swap time mendekati 0 karena sudah dimuat di turn sebelumnya
                metrics["t_swap_sec"] = 0.0

            # --- TAHAP 2: INFERENSI MODEL ---
            t_start_infer = time.perf_counter()
            async with httpx.AsyncClient() as client:
                infer_resp = await client.post(f"{target['endpoint']}{target['infer_path']}", json=payload, timeout=60.0)
            
            metrics["t_infer_sec"] = time.perf_counter() - t_start_infer
            
            # --- TAHAP 3: CLEANUP / UNLOAD (Jika Naive) ---
            if strategy_type == "NAIVE_LOAD_UNLOAD":
                async with httpx.AsyncClient() as client:
                    await client.post(f"{target['endpoint']}{target['unload_path']}", timeout=10.0)

            metrics["t_e2e_sec"] = time.perf_counter() - t_start_e2e
            metrics["success"] = (infer_resp.status_code == 200)

        except Exception as e:
            metrics["success"] = False
            metrics["error"] = str(e)
            metrics["t_e2e_sec"] = time.perf_counter() - t_start_e2e

        finally:
            monitor_data = self.monitor.stop()
            metrics["v_peak_mb"] = monitor_data["peak_vram_mb"]

        return metrics
```

---

## 5. Kriteria Keberhasilan Modul Resource Management
- [ ] PyNVML berhasil mencuplik alokasi VRAM tanpa kebocoran memori pada thread monitor.
- [ ] Nilai $T_{\text{swap}}$, $T_{\text{infer}}$, dan $T_{\text{e2e}}$ terekam dalam satuan detik berpresisi floating point.
- [ ] VRAM puncak terverifikasi tidak melebihi batas target aman ($\le 7,5\text{ GB}$).
