import streamlit as st
import requests
import sqlite3

# 🎨 Configuración visual estética de la aplicación
st.set_page_config(
    page_title="Fábrica de Contenido IA", page_icon="🚀", layout="centered"
)

st.title("🚀 Creador Automatizado de Contenido")
st.markdown(
    "Escribe una idea simple y la Inteligencia Artificial generará y guardará tus publicaciones."
)
st.markdown("---")

# Datos de conexión con tu servidor local seguro de FastAPI
URL_SERVIDOR = "http://127.0.0.1:8000"
HEADERS_SEGURIDAD = {"x-api-key": "MiContrasenaSecreta123"}

# Diseñamos dos secciones cómodas usando pestañas visuales
tab_crear, tab_historial = st.tabs(["📝 Generar Publicaciones", "🗄️ Ver Historial SQL"])

# =========================================================================
# PESTAÑA 1: GENERAR PUBLICACIONES (Envía datos al servidor)
# =========================================================================
with tab_crear:
    st.subheader("💡 ¿Sobre qué quieres publicar hoy?")

    # Caja de entrada de texto para la idea principal
    idea_usuario = st.text_input(
        "Introduce tu tema o idea base:",
        placeholder="Ej: Las ventajas de usar entornos virtuales en Python",
    )

    if st.button("Activar Fábrica de Contenido", use_container_width=True):
        if not idea_usuario:
            st.warning("⚠️ Por favor, escribe una idea primero.")
        else:
            # Preparamos el formato JSON estructurado que espera la API
            datos_peticion = {"tema_principal": idea_usuario}

            with st.spinner(
                "Conectando con tu servidor... Gemini está redactando tus publicaciones..."
            ):
                try:
                    # Hacemos el puente HTTP POST enviando el token en las cabeceras
                    respuesta = requests.post(
                        f"{URL_SERVIDOR}/generar_contenido",
                        json=datos_peticion,
                        headers=HEADERS_SEGURIDAD,
                    )

                    if respuesta.status_code == 200:
                        resultado = respuesta.json()

                        if resultado.get("estado") == "Error":
                            st.error(
                                f"🚨 Fallo interno del servidor: {resultado.get('detalle')}"
                            )
                        else:
                            st.success(
                                "🎉 ¡Contenido generado y almacenado con éxito en la Base de Datos!"
                            )

                            # Mostramos los diseños finales en cajas elegantes
                            st.markdown("### 🐦 Versión para Twitter (X)")
                            st.info(resultado.get("twitter"))

                            st.markdown("### 💼 Versión para LinkedIn")
                            st.code(resultado.get("linkedin"), language="text")
                    else:
                        st.error(
                            f"❌ Error de comunicación ({respuesta.status_code}): {respuesta.text}"
                        )

                except Exception as e:
                    st.error(
                        "🔌 No se pudo conectar con el servidor backend. Verifica que la consola de Uvicorn siga encendida."
                    )

# =========================================================================
# PESTAÑA 2: VER HISTORIAL SQL (Consulta la base de datos local)
# =========================================================================
with tab_historial:
    st.subheader("📋 Archivo de Publicaciones Guardadas")
    st.markdown(
        "Estos datos se leen directamente desde el archivo `contenido_redes.db` de tu disco duro."
    )

    if st.button("Actualizar Historial", use_container_width=True):
        try:
            # Nos conectamos de forma local para leer lo que ha guardado el servidor
            conexion = sqlite3.connect("contenido_redes.db")
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, tema, post_twitter, post_linkedin, fecha FROM publicaciones ORDER BY id DESC"
            )
            filas = cursor.fetchall()
            conexion.close()

            if filas:
                # Formateamos los registros para mostrarlos en una tabla limpia de Streamlit
                tabla_datos = []
                for f in filas:
                    tabla_datos.append(
                        {
                            "ID": f[0],
                            "Tema Original": f[1],
                            "Twitter": f[2],
                            "LinkedIn": f[3],
                            "Fecha de Creación": f[4],
                        }
                    )
                st.dataframe(tabla_datos, use_container_width=True)
            else:
                st.info(
                    "💡 La base de datos está limpia. Genera tu primer contenido en la pestaña anterior."
                )
        except Exception as e:
            st.error(f"🚨 No se pudo leer la base de datos: {str(e)}")
