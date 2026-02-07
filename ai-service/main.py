from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from gemini_client import generate_explanation

app = FastAPI(title="OBD++ AI Service")

# ---- Request schema ----
class GenerateRequest(BaseModel):
    code: str
    dtc_info: dict
    freeze_frame: dict

# ---- Response schema ----
class GenerateResponse(BaseModel):
    explanation: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        explanation = generate_explanation(
            code=req.code,
            dtc_info=req.dtc_info,
            freeze_frame=req.freeze_frame
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
