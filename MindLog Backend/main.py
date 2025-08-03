from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import generate_ai_response
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["https://mindproject.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos esperado
class AIRequest(BaseModel):
    message: str
    style: str = "psychologist"  # Valores: psychologist, coach, friend
    language: str = "es"         # Valores: es, en, gl

@app.post("/ai-assistant")
async def ai_assistant(request: AIRequest):
    try:
        reply = await generate_ai_response(
            message=request.message,
            style=request.style,
            language=request.language
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "MindLog backend funcionando"}

