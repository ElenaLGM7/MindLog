import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str) -> str:
    if not openai.api_key:
        return "❌ Error: OpenAI API key not found."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente emocional empático y seguro."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Error al generar respuesta: {str(e)}"
