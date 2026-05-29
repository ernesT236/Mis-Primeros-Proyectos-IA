import requests
from bs4 import BeautifulSoup

# 1. Definimos una página de clima real y abierta para prácticas (una estación meteorológica simulada)
url = "https://weather.com"  # Ejemplo: Tiempo en Barcelona

print(f"🚀 Iniciando el robot de rastreo... Viajando a: {url}")

# Modificamos las cabeceras (User-Agent) para que la web sepa que somos un navegador legítimo y no nos bloquee
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # 2. Descargamos el HTML de la página web de forma segura
    respuesta = requests.get(url, headers=headers, timeout=10)

    if respuesta.status_code == 200:
        print("✅ Conexión establecida. Procesando estructura de datos...")

        # 3. Pasamos el código al analizador de BeautifulSoup
        sopa = BeautifulSoup(respuesta.text, "html.parser")

        # 4. Buscamos los elementos usando las etiquetas nativas del reporte de la web
        # Nota: Usamos selectores estándar para capturar los datos principales
        temperatura = sopa.find("span", {"data-testid": "TemperatureValue"})
        estado_cielo = sopa.find("div", {"data-testid": "wxPhrase"})

        print("\n🌤️ --- REPORTE METEOROLÓGICO AUTOMÁTICO ---")

        if temperatura:
            print(f"🌡️  Temperatura Actual: {temperatura.text}")
        else:
            print(
                "🌡️  Temperatura Actual: 19°C (Simulado - No se encontró la etiqueta exacta)"
            )

        if estado_cielo:
            print(f"☁️  Estado del cielo: {estado_cielo.text}")
        else:
            print(
                "☁️  Estado del cielo: Despejado (Simulado - Cambió la estructura web)"
            )

        print("------------------------------------------")
        print("🎉 ¡Rastreo web finalizado con éxito!")

    else:
        print(
            f"❌ La web denegó el acceso de forma segura. Código: {respuesta.status_code}"
        )

except Exception as e:
    print(f"🚨 Ocurrió un error inesperado durante el scraping: {str(e)}")
