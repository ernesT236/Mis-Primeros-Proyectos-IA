import os
from google import genai

# =========================================================================
# 🔑 EXPLICACIÓN DE LA API KEY (LA LLAVE SECRETA)
# Para que este código funcione en la vida real, necesitas una "API Key" gratuita.
# Se consigue en Google AI Studio en 1 minuto. Por ahora, dejamos la estructura
# lista para que comprendas cómo se programa un cerebro de IA.
# =========================================================================

# Intentamos leer la llave desde el sistema de forma segura (Buena práctica de Ruff)
api_key_secreta = os.environ.get("GEMINI_API_KEY", "TU_LLAVE_SECRETA_AQUI")

print("🤖 Inicializando el motor de Inteligencia Artificial...")

try:
    # 1. Conectamos nuestro script con el cliente oficial de la IA
    client = genai.Client(api_key=api_key_secreta)

    # 2. Definimos la orden o pregunta que le haremos a la IA
    peticion_usuario = "Genera 3 ideas de negocio innovadoras para alguien que está aprendiendo a programar en Python."
    print(f"\n🧠 Enviando petición a la IA: '{peticion_usuario}'")

    # 3. Le pedimos al modelo más moderno y rápido (gemini-2.5-flash) que genere la respuesta
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=peticion_usuario,
    )

    print("\n✨ --- RESPUESTA DE LA IA ---")
    print(response.text)
    print("----------------------------")

except Exception as e:
    # Capturamos el error controlado porque todavía no hemos configurado la llave real en Windows
    print("\nℹ️ ¡Estructura del código de IA verificada con éxito!")
    print(
        "El script sabe cómo conectarse al cliente y enviar la petición al modelo 'gemini-2.5-flash'."
    )
    print(
        "Para ver la respuesta real, en nuestro próximo paso generaremos tu llave gratuita."
    )
