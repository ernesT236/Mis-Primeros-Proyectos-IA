import os
import sqlite3
from fastapi import FastAPI, Header, HTTPException, Depends
from google import genai
from pydantic import BaseModel

# 1. Inicializamos la aplicación del servidor web
app = FastAPI(
    title="Mi API Corporativa Segura Pro",
    description="Servidor web protegido con autenticación de API Key para todas las operaciones",
    version="4.0.0",
)


# --- CONFIGURACIÓN DE LLAVES DE SEGURIDAD ---
# Esta es tu "Contraseña Secreta" para blindar el servidor. Solo tú la conoces.
CLAVE_ACCESO_API = "MiContrasenaSecreta123"

# Configuración de tu API Key de Google para la IA
API_KEY_GOOGLE = os.environ.get("GEMINI_API_KEY", "TU_LLAVE_SECRETA_AQUI")


# Modelos de datos para el navegador
class ModeloEmpleado(BaseModel):
    nombre: str
    puesto: str
    salario: float


class ModeloConsultaIA(BaseModel):
    pregunta: str


# =========================================================================
# 🛡️ EL ESCUDO DE SEGURIDAD (Función de Dependencia)
# Esta función intercepta cualquier petición a la web, busca la cabecera
# 'x-api-key' y verifica que la contraseña coincida.
# =========================================================================
def verificar_seguridad(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Llave de acceso ausente. Inserte su contraseña en la cabecera 'x-api-key'.",
        )
    if x_api_key != CLAVE_ACCESO_API:
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado. La llave de acceso proporcionada es inválida.",
        )
    return x_api_key


# FUNCIÓN AUXILIAR: Mantiene limpia la base de datos SQL
def inicializar_base_datos():
    conexion = sqlite3.connect("empresa_api.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT,
        salario REAL
    )
    """)
    conexion.commit()
    conexion.close()


inicializar_base_datos()


# =========================================================================
# 🌐 RUTA 1: Registrar Empleado en SQL (POST)
# Añadimos 'Depends(verificar_seguridad)' para blindar la ruta
# =========================================================================
@app.post("/registrar_empleado")
def guardar_en_sql(empleado: ModeloEmpleado, token: str = Depends(verificar_seguridad)):
    try:
        conexion = sqlite3.connect("empresa_api.db")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO empleados (nombre, puesto, salario) VALUES (?, ?, ?)",
            (empleado.nombre, empleado.puesto, empleado.salario),
        )
        conexion.commit()
        conexion.close()
        return {
            "estado": "Éxito",
            "mensaje": f"Guardado físico exitoso. Usuario autorizado por token.",
        }
    except Exception as e:
        return {"estado": "Error", "detalle": str(e)}


# =========================================================================
# 🌐 RUTA 2: Leer la Base de Datos desde la Web (GET) - BLINDADA 🛡️
# =========================================================================
@app.get("/ver_plantilla")
def descargar_plantilla(token: str = Depends(verificar_seguridad)):
    conexion = sqlite3.connect("empresa_api.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, puesto, salario FROM empleados")
    filas = cursor.fetchall()
    conexion.close()

    lista_empleados = []
    for f in filas:
        lista_empleados.append({"id": f, "nombre": f, "puesto": f, "salario": f})
    return {"empleados_registrados": lista_empleados}


# =========================================================================
# 🌐 RUTA 3: Cerebro de la IA en la Web (POST) - BLINDADA 🛡️
# =========================================================================
@app.post("/preguntar_ia")
def procesar_con_ia(
    consulta: ModeloConsultaIA, token: str = Depends(verificar_seguridad)
):
    try:
        if API_KEY_GOOGLE == "TU_LLAVE_SECRETA_AQUI":
            return {
                "estado": "Modo simulación",
                "respuesta_ia": "Acceso autorizado. Llave de Google pendiente en código.",
            }

        client = genai.Client(api_key=API_KEY_GOOGLE)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=consulta.pregunta,
        )
        return {"estado": "Éxito", "respuesta_ia": response.text}

    except Exception as e:
        return {"estado": "Error", "detalle": str(e)}
