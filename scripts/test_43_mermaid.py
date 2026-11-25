import urllib.request
import base64
from pathlib import Path
from PIL import Image

diag = """flowchart TB
    classDef startEnd fill:#F3F4F6,stroke:#1F2937,stroke-width:1.5px
    classDef ui fill:#FEF9C3,stroke:#CA8A04,stroke-width:1.5px
    classDef orch fill:#E0F2FE,stroke:#0284C7,stroke-width:2px
    classDef rm fill:#F3E8FF,stroke:#9333EA,stroke-width:2px
    classDef ai fill:#DCFCE7,stroke:#16A34A,stroke-width:1.5px
    classDef eval fill:#FEE2E2,stroke:#DC2626,stroke-width:1.5px

    subgraph TOP [ALUR INPUT DAN ORKESTRASI SISTEM]
        direction LR
        subgraph INP [1. Input Pengguna]
            U([Pengguna Kiosk]):::startEnd --> SENS[Sentuhan / Suara / Kamera]:::startEnd
        end

        subgraph TB1 [2. UI/UX Chromium Kiosk]
            UI_PRES[Tampilan Layar Potret 9:16]:::ui --> UI_REQ[Kirim Permintaan Aksi Pengguna]:::ui
        end

        subgraph TB2 [3. Orchestrator]
            GW[API Gateway]:::orch --> ROUTE[Routing dan Seleksi Layanan]:::orch
            ROUTE --> STATE[Manajer Siklus Hidup Model AI]:::orch
        end

        SENS --> UI_PRES
        UI_REQ --> GW
    end

    subgraph BOTTOM [MANAJEMEN SUMBER DAYA, EKSEKUSI AI, DAN EVALUASI]
        direction LR
        subgraph TB3 [4. Resource Management]
            POLICY[Eksekusi Strategi Memori GPU]:::rm <--> MON[Pemantauan VRAM dan RAM via NVML]:::rm
        end

        subgraph AI_EXEC [5. Eksekusi Model AI]
            INFER_EXEC[Inferensi Model AI pada GPU Lokal]:::ai
        end

        subgraph OUTP [6. Output dan Evaluasi]
            RES_DISP[Hasil Respons ke UI Kiosk]:::ui
            LOG_EVAL[Pencatatan 5 Metrik Evaluasi Kinerja]:::eval
        end

        MON --> LOG_EVAL
        INFER_EXEC --> RES_DISP
    end

    STATE <--> POLICY
    STATE --> INFER_EXEC
"""

b64 = base64.urlsafe_b64encode(diag.strip().encode("utf-8")).decode("ascii")
url = f"https://mermaid.ink/img/{b64}?bgColor=!white"

out_path = Path("assets/diagrams/test_43_mermaid.png")
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        out_path.write_bytes(resp.read())
    with Image.open(out_path) as im:
        print(f"Downloaded Mermaid: size = {im.size}, ratio = {im.size[0]/im.size[1]:.2f}")
except Exception as e:
    print("Error:", e)
