from dotenv import load_dotenv
load_dotenv()

from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

import requests
import os

from supabase_client import get_dtc_info


AI_SERVICE_URL = os.environ["AI_SERVICE_URL"]

app = FastAPI(title="OBD++ API Service")

class ExplainRequest(BaseModel):
    code: str
    freeze_frame: dict

class ExplainResponse(BaseModel):
    code: str
    explanation: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/explain", response_model=ExplainResponse)
def explain(
    req: Annotated[ExplainRequest, Body(...)]
):
    # 1. Get DTC info from Supabase
    dtc_info = get_dtc_info(req.code)
    if not dtc_info:
        raise HTTPException(status_code=404, detail="DTC not found")

    # 2. Call AI service
    res = requests.post(
        AI_SERVICE_URL,
        json={
            "code": req.code,
            "dtc_info": dtc_info,
            "freeze_frame": req.freeze_frame
        },
        timeout=60
    )

    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="AI service error")

    explanation = res.json()["explanation"]

    # 3. Return final response
    return {
        "code": req.code,
        "explanation": explanation
    }
