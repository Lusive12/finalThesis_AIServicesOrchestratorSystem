# Smart Kiosk AI Experience

Touchscreen interface for the existing Smart Kiosk orchestration project. The kiosk remains a lightweight HTML/CSS/Vanilla JavaScript app served by the repository's FastAPI gateway. The gateway forwards real requests to the separately deployed adapters in `configs/services.yaml`; the browser never manages service processes or containers.

## Run locally

1. Create and activate a Python virtual environment, then install the pinned project dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the gateway from the project root:

   ```bash
   cp .env.example .env
   set -a && source .env && set +a
   python run.py server --host 0.0.0.0 --port 8000
   ```

3. Open `http://127.0.0.1:8000/ui/` in Chromium. Camera capture requires localhost or HTTPS; file upload remains available if camera access is denied.

Mock mode defaults to `KIOSK_MOCK_MODE=true`. It simulates service startup and returns clearly labeled sample responses; it does not perform image generation, virtual try-on, recommendations, or AI conversation. To connect real services, set `KIOSK_MOCK_MODE=false`, configure adapter endpoints in `configs/services.yaml`, and have each adapter implement the existing `/load`, `/health`, `/unload`, and `/infer` contract. The gateway requests `/load`, polls `/health` until the service reports `READY`, and refuses inference until readiness is confirmed. Per-service browser requests use `/api/services/{id}/{status,start,health,infer}`. Ready polling and inactivity timeout are configurable using `.env.example` values.

Environment variables are read by the process; the example file is not loaded automatically. Export its values in the launch environment (as shown above) or configure the same variables in the service manager.

## Chromium kiosk on Linux

Run the gateway at boot, then launch Chromium with the kiosk URL:

```bash
chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-pinch --overscroll-history-navigation=0 http://127.0.0.1:8000/ui/
```

Use the OS display settings to set the panel to portrait orientation. The interface scales to the available viewport and suppresses page scrolling on the home view. On smaller screens, service panels can scroll vertically. No cloud font, frontend framework, or 3D runtime is required; the geometric hero effect is CSS-only.

## Integration notes

- Public service IDs: `ai_photobooth`, `virtual_tryon`, `fashion_recommender`, and `speech_llm` (conversation maps to the registered `speech_llm` adapter).
- Image payloads currently use a data URL for the adapter request. Adapter request/response schemas can be mapped in `src/orchestrator/kiosk_services.py` when the concrete service contracts are finalized.
- Mock response objects include `mock: true`; successful mock UI states explicitly say “simulasi”.
- `KIOSK_IDLE_TIMEOUT_SECONDS` returns an active screen to home. Camera tracks are stopped when leaving a service.
