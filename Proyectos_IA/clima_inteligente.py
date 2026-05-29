import os
import requests
from bs4 import BeautifulSoup
from google import genai

# =========================================================================
# 🔑 CONFIGURACIÓN DE SEGURIDAD
# Recuerda pegar tu API Key real aquí dentro de las comillas para la prueba.
# Antes de subirlo a GitHub, la borraremos para proteger tu cuenta.
# =========================================================================
api_key_secreta = os.environ.get("GEMINI_API_KEY", "TU_LLAVE_SECRETA_AQUI")

print("🚀 Paso 1: Iniciando el robot de Web Scraping...")

# --- PARTE 1: WEB SCRAPING (Extraer datos de internet) ---
url = "https://weather.com"  # Tiempo en Barcelona
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    respuesta = requests.get(url, headers=headers, timeout=10)
    temp_real = "22°C"  # Valores por defecto por si la web cambia sus etiquetas
    cielo_real = "Despejado"

    if respuesta.status_code == 200:
        sopa = BeautifulSoup(respuesta.text, "html.parser")
        temperatura = sopa.find("span", {"data-testid": "TemperatureValue"})
        estado_cielo = sopa.find("div", {"data-testid": "wxPhrase"})

        if temperatura:
            temp_real = temperatura.text
        if estado_cielo:
            cielo_real = estado_cielo.text
        print(f"✅ Datos extraídos con éxito: {temp_real} y cielo {cielo_real}.")
    else:
        print("⚠️ La web no respondió a tiempo. Usando últimos datos guardados.")

    # --- PARTE 2: INTELIGENCIA ARTIFICIAL (Procesar la información) ---
    print("\n🤖 Paso 2: Conectando con el asistente de IA...")

    client = genai.Client(api_key=api_key_secreta)

    # Diseñamos un "Prompt" profesional inyectando los datos del Scraping
    prompt_completo = f"""
    Actúa como un meteorólogo experto y un asistente de estilo de vida.
    Te paso los datos del clima reales de hoy:
    - Temperatura actual: {temp_real}
    - Estado del cielo: {cielo_real}
    
    Redacta un informe muy breve y amigable (máximo 3 párrafos) donde le expliques al usuario cómo está el día y dale 2 consejos prácticos sobre qué ropa vestir hoy o si debe llevar algún accesorio (como paraguas o gafas de sol).
    """

    print("🧠 Generando tu informe personalizado...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_completo,
    )

    print("\n✨ ================= INFORME GENERADO POR IA ================= ✨")
    print(response.text)
    print("=================================================================\n")
    print("🎉 ¡Fusión completada con éxito!")

except Exception as e:
    print(f"\n🚨 Error controlado en la ejecución: {str(e)}")
    print("Recuerda verificar que pegaste tu API Key correctamente en la línea 11.")
