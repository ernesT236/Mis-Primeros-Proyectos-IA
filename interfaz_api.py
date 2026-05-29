import streamlit as st
import requests

# 🛠️ CONFIGURACIÓN DE LA PANTALLA VISUAL
st.set_page_config(
    page_title="Panel Corporativo - Ernest Pro", page_icon="💼", layout="centered"
)

st.title("💼 Sistema de Gestión Corporativa")
st.markdown(
    "Esta interfaz se comunica en segundo plano con tu servidor web seguro de FastAPI."
)
st.markdown("---")

# 🔐 DATOS DE AUTENTICACIÓN (Se envían ocultos en la cabecera)
URL_API = "http://127.0.0.1:8000"
HEADERS_SEGURIDAD = {"x-api-key": "MiContrasenaSecreta123"}

# Creamos dos pestañas visuales hermosas en la pantalla del usuario
tab_empleados, tab_ia = st.tabs(["📋 Gestión de Empleados", "🧠 Consulta con IA"])

# =========================================================================
# PESTAÑA 1: GESTIÓN DE EMPLEADOS (Conectada a FastAPI + SQL)
# =========================================================================
with tab_empleados:
    st.subheader("➕ Registrar Nuevo Empleado")

    # Formulario visual para el usuario
    with st.form("form_registro", clear_on_submit=True):
        nombre = st.text_input("Nombre Completo:")
        puesto = st.text_input("Puesto o Cargo:")
        salario = st.number_input("Salario Mensual ($):", min_value=0.0, step=100.0)
        boton_enviar = st.form_submit_button(
            "Enviar al Servidor", use_container_width=True
        )

        if boton_enviar:
            if not nombre or not puesto:
                st.error("❌ Todos los campos son obligatorios.")
            else:
                # Preparamos los datos en el formato JSON que la API exige
                datos_json = {"nombre": nombre, "puesto": puesto, "salario": salario}

                try:
                    # Hacemos el puente HTTP POST hacia el servidor enviando el token secreto
                    respuesta = requests.post(
                        f"{URL_API}/registrar_empleado",
                        json=datos_json,
                        headers=HEADERS_SEGURIDAD,
                    )

                    if respuesta.status_code == 200:
                        st.success(
                            f"✅ ¡Servidor responde!: {respuesta.json()['mensaje']}"
                        )
                    else:
                        st.error(
                            f"🚨 Error de Autenticación ({respuesta.status_code}): {respuesta.json()['detail']}"
                        )
                except Exception:
                    st.error(
                        "❌ No se pudo conectar con el servidor web. Asegúrate de que FastAPI esté encendido."
                    )

    # Botón para consultar la base de datos en tiempo real
    st.markdown("---")
    st.subheader("📊 Plantilla Actual")
    if st.button("Actualizar y Leer Base de Datos", use_container_width=True):
        try:
            # Hacemos la petición HTTP GET al servidor
            respuesta = requests.get(
                f"{URL_API}/ver_plantilla", headers=HEADERS_SEGURIDAD
            )

            if respuesta.status_code == 200:
                empleados = respuesta.json()["empleados_registrados"]
                if empleados:
                    st.dataframe(empleados, use_container_width=True)
                else:
                    st.info("💡 El servidor informa que la base de datos está vacía.")
            else:
                st.error(f"🚨 Acceso Denegado: {respuesta.json()['detail']}")
        except Exception:
            st.error("❌ Servidor desconectado.")

# =========================================================================
# PESTAÑA 2: CONSULTA CON IA (Conectada a FastAPI + Gemini)
# =========================================================================
with tab_ia:
    st.subheader("🧠 Preguntar al Servidor de IA")
    pregunta_usuario = st.text_area("Escribe tu consulta para el modelo Gemini:")

    if st.button("Consultar Inteligencia Artificial", use_container_width=True):
        if not pregunta_usuario:
            st.warning("⚠️ Escribe una pregunta primero.")
        else:
            datos_ia = {"pregunta": pregunta_usuario}
            with st.spinner("El servidor está procesando la respuesta con la IA..."):
                try:
                    # Conectamos con la ruta de la IA enviando la contraseña
                    respuesta = requests.post(
                        f"{URL_API}/preguntar_ia",
                        json=datos_ia,
                        headers=HEADERS_SEGURIDAD,
                    )

                    if respuesta.status_code == 200:
                        st.markdown("### 📝 Respuesta Recibida:")
                        st.info(respuesta.json()["respuesta_ia"])
                    else:
                        st.error(f"🚨 Error: {respuesta.json()['detail']}")
                except Exception:
                    st.error("❌ Error de conexión con el servidor.")
