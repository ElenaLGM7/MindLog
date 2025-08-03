print("🟢 Starting MindLog backend...")

from fastapi import FastAPI
# resto de imports...

app = FastAPI()

print("🟢 FastAPI app created successfully")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from ai import generate_response
from database import create_tables, save_entry
from utils import get_current_datetime
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Montar frontend si lo deseas desde el backend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Crear tablas si no existen
create_tables()

class EntryRequest(BaseModel):
    text: str
    emotions: list[str] = []
    date: str | None = None

@app.post("/generate")
async def chat(entry: EntryRequest):
    response = generate_response(entry.text)
    timestamp = get_current_datetime()
    save_entry(entry.text, entry.emotions, timestamp)
    return {"response": response, "timestamp": timestamp}
