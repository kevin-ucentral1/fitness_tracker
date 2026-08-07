import streamlit as st
from database import conectar

st.set_page_config(page_title="Fitness Tracker", page_icon="🏋️", layout="wide")

# ---------------------------------
# MENÚ LATERAL
# ---------------------------------
menu = st.sidebar.radio("Menú principal", ["🏋️ Gym", "💳 Gastos", "🔒 Cerrar sesión"])

# ---------------------------------
# CONTROL DE ACCESO
# ---------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Fitness Tracker")
    clave = st.text_input("Código de acceso", type="password")
    if st.button("Ingresar"):
        if clave == st.secrets["app"]["password"]:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ Código incorrecto")
    st.stop()

# ---------------------------------
# SECCIÓN GYM
# ---------------------------------
if menu == "🏋️ Gym":
    st.title("🏋️ Registro de Entrenamiento")
    if "entrenamiento" not in st.session_state:
        st.session_state.entrenamiento = []

    ejercicio = st.text_input("Ejercicio")
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.5)
    series = st.number_input("Series", min_value=1, step=1)
    repeticiones = st.number_input("Repeticiones", min_value=1, step=1)

    if st.button("Agregar ejercicio"):
        st.session_state.entrenamiento.append({
            "ejercicio": ejercicio,
            "peso": peso,
            "series": series,
            "repeticiones": repeticiones
        })
        st.success("✅ Ejercicio agregado")

    st.subheader("📋 Entrenamiento actual")
    st.table(st.session_state.entrenamiento)

    if st.button("💾 Guardar entrenamiento"):
        conn = conectar()
        cursor = conn.cursor()
        for e in st.session_state.entrenamiento:
            cursor.execute("""
                INSERT INTO entrenamiento (ejercicio, peso, series, repeticiones)
                VALUES (%s, %s, %s, %s)
            """, (e["ejercicio"], e["peso"], e["series"], e["repeticiones"]))
        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.entrenamiento = []
        st.success("✅ Entrenamiento guardado")

# ---------------------------------
# SECCIÓN GASTOS
# ---------------------------------
elif menu == "💳 Gastos":
    st.title("💳 Registro de Gastos")
    if "gastos" not in st.session_state:
        st.session_state.gastos = []

    monto = st.number_input("Monto del gasto", min_value=0.0, step=100.0)
    descripcion = st.text_input("Descripción")

    if st.button("Registrar gasto"):
        st.session_state.gastos.append({"monto": monto, "descripcion": descripcion})
        st.success("✅ Gasto registrado")

    st.subheader("📋 Historial de gastos")
    st.table(st.session_state.gastos)

    if st.button("💾 Guardar gastos"):
        conn = conectar()
        cursor = conn.cursor()
        for g in st.session_state.gastos:
            cursor.execute("""
                INSERT INTO gastos (monto, descripcion)
                VALUES (%s, %s)
            """, (g["monto"], g["descripcion"]))
        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.gastos = []
        st.success("✅ Gastos guardados")

# ---------------------------------
# CERRAR SESIÓN
# ---------------------------------
elif menu == "🔒 Cerrar sesión":
    st.session_state.login = False
    st.session_state.entrenamiento = []
    st.session_state.gastos = []
    st.rerun()
