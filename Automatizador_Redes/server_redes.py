import os
import sqlite3
from datetime import datetime
from fastapi import Depends, FastAPI, Header, HTTPException
from google import genai
from pydantic import BaseModel

app = FastAPI(
    title="API Generadora de Contenido Pro",
    description="Servidor inteligente para redactar y almacenar posts corporativos",
    version="1.0.0",
)

# 🔐 Medidas de seguridad y claves
CLAVE_ACCESO_API = "MiContrasenaSecreta123"
API_KEY_GOOGLE = os.environ.get("GEMINI_API_KEY", "TU_LLAVE_SECRETA_AQUI")


class ModeloIdea(BaseModel):
    tema_principal: str


def verificar_seguridad(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key != CLAVE_ACCESO_API:
        raise HTTPException(status_code=403, detail="Token inválido o ausente.")
    return x_api_key


def inicializar_bd():
    conexion = sqlite3.connect("contenido_redes.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publicaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema TEXT,
        post_twitter TEXT,
        post_linkedin TEXT,
        fecha TEXT
    )
    """)
    conexion.commit()
    conexion.close()


inicializar_bd()


@app.post("/generar_contenido")
def crear_contenido(idea: ModeloIdea, token: str = Depends(verificar_seguridad)):
    try:
        # 1. Modo Simulación si falta la llave
        if API_KEY_GOOGLE == "TU_LLAVE_SECRETA_AQUI":
            return {
                "estado": "Simulación",
                "twitter": f"Post de Twitter sobre {idea.tema_principal} (Simulado)",
                "linkedin": f"Post de LinkedIn sobre {idea.tema_principal} (Simulado)",
            }

        # 2. Conexión real con Gemini
        client = genai.Client(api_key=API_KEY_GOOGLE)

        prompt = f"""
        Actúa como un Copywriter y Community Manager experto.
        El usuario te da un tema: '{idea.tema_principal}'.
        
        Redacta dos publicaciones profesionales:
        1. Para Twitter (máximo 280 caracteres, directo, usa hashtags).
        2. Para LinkedIn (más extenso, profesional, reflexivo, con saltos de línea).
        
        Devuelve la respuesta estrictamente separada por la palabra clave "---DIVISOR---" (sin comillas) entre el post de Twitter y el de LinkedIn. No agregues introducciones ni textos extra.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        texto_ia = response.text
        partes = texto_ia.split("---DIVISOR---")

        twitter_final = partes[0].strip() if len(partes) > 0 else texto_ia
        linkedin_final = partes[1].strip() if len(partes) > 1 else texto_ia

        # 3. Guardar físicamente en SQL
        conexion = sqlite3.connect("contenido_redes.db")
        cursor = conexion.cursor()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor.execute(
            """
        INSERT INTO publicaciones (tema, post_twitter, post_linkedin, fecha)
        VALUES (?, ?, ?, ?)
        """,
            (idea.tema_principal, twitter_final, linkedin_final, fecha_hoy),
        )

        conexion.commit()
        conexion.close()

        return {
            "estado": "Éxito",
            "twitter": twitter_final,
            "linkedin": linkedin_final,
        }

    except Exception as e:
        return {"estado": "Error", "detalle": str(e)}
