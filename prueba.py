import openai

# Conexión directa a tu Ollama local
client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

try:
    print("Enviando pregunta a Ollama... por favor espera.")
    # Usamos qwen2.5-coder:7b que es tu modelo activo
    respuesta = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": "¡Hola! Salúdame en español de forma muy corta.",
            }
        ],
    )
    print("\n--- Respuesta de tu IA ---")
    print(respuesta.choices[0].message.content)
except Exception as e:
    print(f"\nOcurrió un error: {e}")
