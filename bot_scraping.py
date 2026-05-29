import pandas as pd
from bs4 import BeautifulSoup
import requests

# 1. Definimos la página web que queremos escanear
url = "https://toscrape.com"

print(f"🚀 El bot está viajando a: {url}...")

# 2. Hacemos la petición a internet para descargar el código HTML de la web
respuesta = requests.get(url)

# Verificamos si la web nos dio permiso para entrar (Código 200 significa OK)
if respuesta.status_code == 200:
    print("✅ Conexión exitosa. Extrayendo información...\n")

    # 3. Le pasamos el HTML descargado a BeautifulSoup para que lo pueda leer fácilmente
    sopa = BeautifulSoup(respuesta.text, "html.parser")

    # 4. Buscamos todas las cajas de texto que contienen las citas
    cajas_citas = sopa.find_all("div", class_="quote")

    lista_frases = []
    lista_autores = []

    # 5. Iteramos por cada caja para extraer el texto limpio de la frase y el autor
    for caja in cajas_citas:
        # Extraemos el texto de la frase (está dentro de una etiqueta <span class="text">)
        frase = caja.find("span", class_="text").text

        # Extraemos el nombre del autor (está dentro de una etiqueta <small class="author">)
        autor = caja.find("small", class_="author").text

        lista_frases.append(frase)
        lista_autores.append(autor)

        print(f"✍️ Autor: {autor}")
        print(f"💬 Frase: {frase}")
        print("-" * 50)

    # 6. AUTOMATIZACIÓN EXTRA: Guardamos todo lo extraído en un archivo Excel/CSV limpio
    datos_extraidos = {"Autor": lista_autores, "Frase": lista_frases}
    df = pd.DataFrame(datos_extraidos)
    df.to_csv("citas_extraidas.csv", index=False, encoding="utf-8")
    print(
        "\n🎉 ¡Proceso terminado con éxito! Se ha creado el archivo 'citas_extraidas.csv'."
    )

else:
    print(
        f"❌ Error al intentar conectar con la web. Código de estado: {respuesta.status_code}"
    )
