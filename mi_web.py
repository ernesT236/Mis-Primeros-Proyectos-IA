import os
import pandas as pd
import streamlit as st

# 🛠️ CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera línea de Streamlit)
st.set_page_config(page_title="Panel Financiero Pro", page_icon="💰", layout="wide")

st.title("💼 Mi Panel de Control Financiero Pro")
st.markdown("---")

# 📊 PROCESAMIENTO DE DATOS (Lo hacemos al inicio para usar los datos en todo el diseño)
datos_listos = False
total_gastado = 0.0
resumen_web = pd.DataFrame()

try:
    if os.path.exists("gastos_banco.txt") and os.path.getsize("gastos_banco.txt") > 0:
        df_web = pd.read_csv("gastos_banco.txt", names=["Categoria", "Monto"])
        df_web = df_web.dropna()
        resumen_web = df_web.groupby("Categoria")["Monto"].sum().reset_index()
        total_gastado = resumen_web["Monto"].sum()
        datos_listos = True
except Exception as e:
    st.error(f"🚨 Error al procesar la base de datos: {str(e)}")

# =========================================================================
# 🏢 DISEÑO INTERFAZ: DISEÑO EN 2 COLUMNAS PRINCIPALES
# =========================================================================
col_izquierda, col_derecha = st.columns([1, 2], gap="large")

# 📥 COLUMNA IZQUIERDA: FORMULARIOS Y ACCIONES
with col_izquierda:
    st.subheader("📥 Gestión de Datos")

    with st.form("formulario_gastos", clear_on_submit=True):
        st.markdown("### ➕ Registrar Gasto")
        nueva_cat = st.text_input("Categoría (ej. Comida, Internet):").strip()
        nuevo_monto = st.number_input("Monto gastado ($):", step=1.0)
        boton_guardar = st.form_submit_button("Guardar Gasto", use_container_width=True)

        if boton_guardar:
            if not nueva_cat:
                st.error("❌ La categoría no puede estar vacía.")
            elif nuevo_monto <= 0:
                st.error("❌ El monto debe ser mayor a $0.")
            else:
                try:
                    with open("gastos_banco.txt", "a") as archivo:
                        archivo.write(f"\n{nueva_cat.capitalize()},{nuevo_monto}")
                    st.success(f"✅ ¡{nueva_cat.capitalize()} guardado!")
                    st.rerun()
                except IOError:
                    st.error("❌ Error al guardar en el disco.")

    # 🗑️ SECCIÓN DE BORRADO EN LA BARRA LATERAL (Para dejar la pantalla principal limpia)
    st.markdown("---")
    st.subheader("⚙️ Configuración")
    with st.expander("⚠️ Zona de Peligro"):
        st.write("Esta acción no se puede deshacer.")
        boton_borrar = st.button(
            "Borrar todo el Historial", type="primary", use_container_width=True
        )
        if boton_borrar:
            try:
                with open("gastos_banco.txt", "w") as archivo:
                    archivo.write("")
                st.warning("🗑️ Historial eliminado.")
                st.rerun()
            except IOError:
                st.error("❌ No se pudo limpiar el archivo.")

# 📈 COLUMNA DERECHA: MÉTRICAS, TABLAS Y GRÁFICOS
with col_derecha:
    st.subheader("📊 Visualización de Resultados")

    if datos_listos:
        # Mini-columnas internas para las tarjetas de métricas
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="💰 Total Gastado", value=f"${total_gastado:,.2f}")
        with m2:
            num_categorias = len(resumen_web)
            st.metric(label="🗂️ Categorías Activas", value=num_categorias)
        with m3:
            max_gasto = resumen_web["Monto"].max()
            cat_max = resumen_web.loc[
                resumen_web["Monto"] == max_gasto, "Categoria"
            ].values[0]
            st.metric(label="🔥 Mayor Gasto", value=f"{cat_max} (${max_gasto:,.0f})")

        st.markdown("---")

        # Dividimos el gráfico y la tabla lado a lado
        g1, g2 = st.columns([3, 2])
        with g1:
            st.markdown("#### 📈 Distribución Visual")
            st.bar_chart(
                data=resumen_web,
                x="Categoria",
                y="Monto",
                color="#3498db",
                use_container_width=True,
            )
        with g2:
            st.markdown("#### 📋 Detalle en Tabla")
            st.dataframe(resumen_web.set_index("Categoria"), use_container_width=True)
    else:
        st.info(
            "💡 Aún no hay datos guardados. Agrega tu primer gasto a la izquierda para activar el panel."
        )
