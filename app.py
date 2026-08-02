import streamlit as st
from database import conectar

# ---------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------
st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏋️",
    layout="centered"
)

# ---------------------------------
# ESTILOS CSS
# ---------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #2c3e50;
        text-align: center;
    }
    .justificado {
        text-align: justify;
        color: #34495e;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------
# CONTROL DE ACCESO
# ---------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Fitness Tracker")
    st.markdown("<p class='justificado'>Bienvenido. Ingresa tu código de acceso para continuar.</p>", unsafe_allow_html=True)

    clave = st.text_input("Código de acceso", type="password")

    if st.button("Ingresar"):
        if clave == st.secrets["app"]["password"]:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ Código incorrecto")
    st.stop()

# ---------------------------------
# APLICACIÓN PRINCIPAL
# ---------------------------------
st.title("🏋️ Registro de Entrenamiento")
st.markdown("<p class='justificado'>Aquí puedes registrar tus ejercicios diarios y llevar un control visual de tu progreso.</p>", unsafe_allow_html=True)

# Inicializar sesión
if "entrenamiento" not in st.session_state:
    st.session_state.entrenamiento = []

# ---------------------------------
# AGREGAR EJERCICIO
# ---------------------------------
st.subheader("➕ Registrar ejercicio")

col1, col2 = st.columns(2)
with col1:
    ejercicio = st.text_input("Ejercicio")
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.5)
with col2:
    series = st.number_input("Series", min_value=1, step=1)
    repeticiones = st.number_input("Repeticiones", min_value=1, step=1)

if st.button("Agregar ejercicio"):
    if ejercicio:
        st.session_state.entrenamiento.append({
            "ejercicio": ejercicio,
            "peso": peso,
            "series": series,
            "repeticiones": repeticiones
        })
        st.success(f"{ejercicio} agregado correctamente ✅")
    else:
        st.warning("Ingrese un ejercicio")

# ---------------------------------
# MOSTRAR ENTRENAMIENTO
# ---------------------------------
st.divider()
st.subheader("📋 Entrenamiento actual")

if len(st.session_state.entrenamiento) == 0:
    st.info("No hay ejercicios agregados")
else:
    for i, e in enumerate(st.session_state.entrenamiento, start=1):
        st.markdown(f"""
        <div class='justificado'>
        <b>{i}. {e['ejercicio']}</b><br>
        Peso: {e['peso']} kg | Series: {e['series']} | Repeticiones: {e['repeticiones']}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------
# GUARDAR EN SUPABASE
# ---------------------------------
st.divider()
if st.button("💾 Finalizar entrenamiento"):
    if len(st.session_state.entrenamiento) == 0:
        st.warning("No hay datos para guardar")
    else:
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
        st.success("✅ Entrenamiento guardado correctamente")

# ---------------------------------
# CERRAR SESIÓN
# ---------------------------------
st.divider()
if st.button("🔒 Cerrar sesión"):
    st.session_state.login = False
    st.session_state.entrenamiento = []
    st.rerun()
