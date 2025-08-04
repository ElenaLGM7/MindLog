from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai

# Configuración temporal (sin .env)
openai.api_key = "TU_API_KEY_AQUI"  # ponla aquí directamente por ahora

app = FastAPI()

# CORS para conectar con Netlify/local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend estático
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")

# Endpoint de IA
@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return JSONResponse({"error": "No message received"}, status_code=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o "gpt-4"
            messages=[
                {"role": "system", "content": "Eres un asistente emocional y empático que ayuda a reflexionar."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_reply = response.choices[0].message["content"]
        return {"response": ai_reply.strip()}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
