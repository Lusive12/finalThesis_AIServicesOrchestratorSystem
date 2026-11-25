import urllib.request
import base64

diagram1 = """flowchart LR
    subgraph INP [1. Input Pengguna]
        U([Pengguna Kiosk]) --> SENS[Sentuhan / Suara / Kamera]
    end

    subgraph TB1 [2. UI/UX Chromium Kiosk]
        SENS --> UI_PRES[Tampilan Potret 9:16]
        UI_PRES --> UI_REQ[Kirim Permintaan Aksi]
    end

    subgraph TB2 [3. Orchestrator]
        UI_REQ --> GW[API Gateway]
        GW --> ROUTE[Routing dan Seleksi Layanan]
        ROUTE --> STATE[Manajer Siklus Hidup Model]
    end

    subgraph TB3 [4. Resource Management]
        STATE <--> POLICY[Eksekusi Strategi Memori]
        POLICY <--> MON[Monitor GPU dan RAM via NVML]
    end

    subgraph AI_EXEC [5. Eksekusi Model AI]
        STATE --> INFER_EXEC[Inferensi Model AI pada GPU]
    end

    subgraph OUTP [6. Output dan Evaluasi]
        INFER_EXEC --> RES_DISP[Hasil Layanan ke UI]
        MON --> LOG_EVAL[Pencatatan 5 Metrik Evaluasi]
    end
"""

b64 = base64.urlsafe_b64encode(diagram1.strip().encode("utf-8")).decode("ascii")
url = f"https://mermaid.ink/img/{b64}?bgColor=!white"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        print("Success, bytes:", len(resp.read()))
except Exception as e:
    print("Failed:", e)
