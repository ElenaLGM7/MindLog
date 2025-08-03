import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Definición de estilos de respuesta
STYLE_PRESETS = {
    "psychologist": {
        "es": "Actúa como un psicólogo empático que escucha activamente, valida las emociones y ofrece guía emocional con cuidado.",
        "en": "Act as an empathetic psychologist who listens actively, validates emotions, and offers emotional guidance with care.",
        "gl": "Actúa como un psicólogo empático que escoita activamente, valida as emocións e ofrece orientación emocional con coidado."
    },
    "coach": {
        "es": "Actúa como un coach motivacional que ayuda al usuario a encontrar soluciones prácticas y a empoderarse.",
        "en": "Act as a motivational coach who helps the user find practical solutions and empowers them.",
        "gl": "Actúa como un adestrador motivacional que axuda ao usuario a atopar solucións prácticas e empodérase."
    },
    "friend": {
        "es": "Actúa como un amigo cercano que escucha sin juzgar, ofrece apoyo emocional y ánimos.",
        "en": "Act as a close friend who listens without judgment, offers emotional support and encouragement.",
        "gl": "Actúa como un amigo próximo que escoita sen xuízos, ofrece apoio emocional e ánimo."
    }
}

async def generate_ai_response(message: str, style: str, language: str) -> str:
    system_prompt = STYLE_PRESETS.get(style, STYLE_PRESETS["psychologist"]).get(language, STYLE_PRESETS["psychologist"]["es"])

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Puedes usar "gpt-3.5-turbo" si prefieres
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.8,
        max_tokens=500
    )

    reply = response.choices[0].message.content.strip()
    return reply
