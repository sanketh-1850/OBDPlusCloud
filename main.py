from fastapi import FastAPI, HTTPException, Request
import threading
import time
import requests
from datetime import datetime

from postgres_client import get_dtc_info
from gemini_client import generate_explanation

app = FastAPI(title="OBD++ Cloud Backend")



# --------------------------------------------------------
# 1. Lightweight ping endpoint (Render-friendly)
# --------------------------------------------------------
@app.get("/ping")
def ping():
    return {"ok": True}

# --------------------------------------------------------
# 2. Keep-align function (self-ping)
# --------------------------------------------------------
RENDER_URL = "https://obdpluscloud.onrender.com/ping"  # your Render URL

def keep_alive():
    while True:
        try:
            res = requests.get(RENDER_URL, timeout=10)
            print("PING:", res.status_code, datetime.now())
        except Exception as e:
            print("Ping error:", e)
        time.sleep(600)  # every 1 minute

# --------------------------------------------------------
# 3. Start keep-alive background thread on startup
# --------------------------------------------------------
@app.on_event("startup")
def start_keep_alive_thread():
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    print("🔥 Keep-alive thread started")



@app.get("/")
def home():
    return {"status": "OBD++ cloud backend running"}

@app.post("/explain")
async def explain(request: Request):
    """
    Receives:
      {
        "code": "P0171",
        "freeze_frame": { ... }
      }
    Returns:
      {
        "code": "P0171",
        "explanation": "..."
      }
    """
    data = await request.json()
    code = data.get("code")
    freeze_frame = data.get("freeze_frame", {})

    if not code:
        raise HTTPException(status_code=400, detail="Missing DTC code")

    # fetch dtc info from PostgreSQL
    dtc_info = get_dtc_info(code)
    if not dtc_info:
        raise HTTPException(status_code=404, detail=f"No info found for {code}")

    # generate explanation using Gemini
    result = generate_explanation(code, dtc_info, freeze_frame)

    return {"code": code, "explanation": result}