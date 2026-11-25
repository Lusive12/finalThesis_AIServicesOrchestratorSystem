# 07_BENCHMARK_EVALUATION.md — Otomasi Pengujian & Benchmark Evaluasi (Bab IV)

> **Bagian dari:** [implementation.md](file:///c:/Users/User/Documents/AntiGravity/proof-concept-smartkiosk/implementation.md)  
> **Tahap:** Evaluasi Eksperimental Kuantitatif & Benchmark Komparatif  
> **Target:** Otomasi Pengujian 4 Strategi, Uji Stabilitas 100 Giliran, Ekspor Log CSV/JSONL

---

## 1. Tujuan Dokumen
1. Menyediakan skrip otomatisasi benchmark (*automated test harness*) untuk membandingkan empat strategi pengelolaan model GPU secara terkontrol dan objektif.
2. Memastikan protokol pengujian memenuhi kaidah ilmiah:
   - Pengulangan pengujian minimal **10 kali per kondisi** ($N \ge 10$).
   - Pengujian stabilitas hingga **100 giliran interaksi berturut-turut**.
3. Menyimpan seluruh data mentah ke dalam direktori `results/` dalam format CSV dan JSONL untuk dianalisis pada Bab IV skripsi.

---

## 2. Struktur Direktori Hasil Pengujian (`results/`)

```text
results/
├── benchmark_20261102_strategy_a.csv
├── benchmark_20261102_strategy_b.csv
├── benchmark_20261102_strategy_c.csv
├── benchmark_20261102_strategy_d.csv
├── stability_100_turns.jsonl
└── summary_statistics.json
```

---

## 3. Skrip Otomasi Benchmark Komparatif (`experiments/run_benchmark.py`)

Simpan skrip pengujian ini pada `experiments/run_benchmark.py`:

```python
import time
import csv
import json
import asyncio
from datetime import datetime
from src.resource_manager.strategy_executor import StrategyExecutor

STRATEGIES = ["ALL_RESIDENT", "NAIVE_LOAD_UNLOAD", "PINNED_SWAP", "PREFETCH"]
SERVICES_TO_TEST = ["speech_pipeline", "fashion_recommendation", "virtual_tryon", "photobooth"]
REPETITIONS = 10

async def run_benchmark():
    # Inisialisasi executor
    with open("configs/services.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    executor = StrategyExecutor(config["services"])
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"results/benchmark_{timestamp_str}.csv"

    fieldnames = ["timestamp", "strategy", "repetition", "service_id", "t_swap_sec", "t_infer_sec", "t_e2e_sec", "v_peak_mb", "success"]
    
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for strategy in STRATEGIES:
            print(f"\n==========================================")
            print(f"Mengeksekusi Pengujian: Strategi {strategy}")
            print(f"==========================================")

            for rep in range(1, REPETITIONS + 1):
                print(f"--- Pengulangan {rep}/{REPETITIONS} ---")
                
                for service_id in SERVICES_TO_TEST:
                    payload = {"test_mode": True, "input": "sample_data"}
                    
                    # Jalankan turn pengujian
                    res = await executor.execute_turn(strategy, service_id, payload)
                    
                    row = {
                        "timestamp": datetime.now().isoformat(),
                        "strategy": strategy,
                        "repetition": rep,
                        "service_id": service_id,
                        "t_swap_sec": round(res["t_swap_sec"], 4),
                        "t_infer_sec": round(res["t_infer_sec"], 4),
                        "t_e2e_sec": round(res["t_e2e_sec"], 4),
                        "v_peak_mb": round(res["v_peak_mb"], 2),
                        "success": res["success"]
                    }
                    writer.writerow(row)
                    csv_file.flush()
                    
                    print(f"[{strategy}] {service_id} | Swap: {row['t_swap_sec']}s | Infer: {row['t_infer_sec']}s | VRAM: {row['v_peak_mb']} MB")
                    await asyncio.sleep(1.0) # Jeda antar-layanan

    print(f"\nPengujian selesai! Log tersimpan di: {output_csv}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
```

---

## 4. Protokol Uji Stabilitas 100 Giliran Interaksi

Untuk menguji **Pilar Metrik 5 (Stability Rate)**:
1. Skrip pengujian menjalankan 100 permintaan berturut-turut yang mensimulasikan pengguna acak:
   - 60% Percakapan Suara
   - 20% Rekomendasi Busana
   - 10% Virtual Try-On
   - 10% Photobooth
2. Setiap giliran mencatat:
   - Apakah terjadi CUDA OOM.
   - Apakah terjadi proses crash atau timeout.
   - Tren degradasi waktu latensi.
3. Rumus Tingkat Kestabilan:
   $$R_{\text{stab}} = \left( \frac{N_{\text{sukses}}}{100} \right) \times 100\%$$
   *Target Keberhasilan PoC:* $R_{\text{stab}} = 100\%$ tanpa OOM dan $V_{\text{peak}} \le 7,5\text{ GB}$.

---

## 5. Skrip Agregasi Statistik Deskriptif (`experiments/calculate_stats.py`)

Skrip ini membaca file CSV pengujian dan menghitung rata-rata (*mean*), median, simpangan baku (*standard deviation*), nilai minimum, dan nilai maksimum untuk disajikan pada tabel Bab IV:

```python
import pandas as pd
import sys

def summarize_results(csv_path):
    df = pd.read_csv(csv_path)
    
    # Kelompokkan berdasarkan strategi dan layanan
    summary = df.groupby(["strategy", "service_id"]).agg({
        "t_e2e_sec": ["mean", "median", "std", "min", "max"],
        "t_swap_sec": ["mean", "std"],
        "t_infer_sec": ["mean", "std"],
        "v_peak_mb": ["max", "mean"],
        "success": ["count", "sum"]
    })
    
    print("\n--- RINGKASAN METRIK EVALUASI ---")
    print(summary)
    summary.to_csv("results/summary_table_bab4.csv")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        summarize_results(sys.argv[1])
    else:
        print("Penggunaan: python calculate_stats.py results/benchmark_XXXXX.csv")
```

---

## 6. Kriteria Keberhasilan Evaluasi
- [ ] Pengujian minimal 10 kali pengulangan per kondisi selesai dieksekusi tanpa interupsi manual.
- [ ] Log tersimpan lengkap dengan metadata hardware, waktu, dan commit Git.
- [ ] Berkas `results/summary_table_bab4.csv` terbuat dan siap dikutip ke naskah skripsi Bab IV.
