import streamlit as st
from database import conectar


#----------------prueba temporarl--------




# ---------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------

import streamlit as st
from database import conectar


# ---------------------------------
# CONFIGURACIÓN
# ---------------------------------

st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏋️"
)


# ---------------------------------
# CONTROL DE ACCESO
# ---------------------------------

if "login" not in st.session_state:
    st.session_state.login = False


if not st.session_state.login:

    st.title("🔐 Fitness Tracker")

    clave = st.text_input(
        "Código de acceso",
        type="password"
    )


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

st.title("🏋️ Fitness Tracker")

st.write("Registro de entrenamiento")


# Inicializar sesión

if "entrenamiento" not in st.session_state:

    st.session_state.entrenamiento = []



# ---------------------------------
# AGREGAR EJERCICIO
# ---------------------------------

st.subheader("➕ Registrar ejercicio")


ejercicio = st.text_input(
    "Ejercicio"
)


peso = st.number_input(
    "Peso (kg)",
    min_value=0.0,
    step=0.5
)


series = st.number_input(
    "Series",
    min_value=1,
    step=1
)


repeticiones = st.number_input(
    "Repeticiones",
    min_value=1,
    step=1
)



if st.button("Agregar ejercicio"):

    if ejercicio:

        st.session_state.entrenamiento.append(
            {
                "ejercicio": ejercicio,
                "peso": peso,
                "series": series,
                "repeticiones": repeticiones
            }
        )

        st.success(
            f"{ejercicio} agregado"
        )

    else:

        st.warning(
            "Ingrese un ejercicio"
        )



# ---------------------------------
# MOSTRAR ENTRENAMIENTO
# ---------------------------------

st.divider()

st.subheader("📋 Entrenamiento actual")


if len(st.session_state.entrenamiento) == 0:

    st.info(
        "No hay ejercicios agregados"
    )


else:

    for i, e in enumerate(
        st.session_state.entrenamiento,
        start=1
    ):

        st.write(
            f"""
            **{i}. {e['ejercicio']}**

            Peso: {e['peso']} kg  
            Series: {e['series']}  
            Repeticiones: {e['repeticiones']}
            """
        )



# ---------------------------------
# GUARDAR EN SUPABASE
# ---------------------------------

st.divider()


if st.button("💾 Finalizar entrenamiento"):


    if len(st.session_state.entrenamiento) == 0:

        st.warning(
            "No hay datos para guardar"
        )


    else:

        conn = conectar()

        cursor = conn.cursor()


        for e in st.session_state.entrenamiento:

            cursor.execute(
                """
                INSERT INTO entrenamiento
                (
                    ejercicio,
                    peso,
                    series,
                    repeticiones
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    e["ejercicio"],
                    e["peso"],
                    e["series"],
                    e["repeticiones"]
                )
            )


        conn.commit()

        cursor.close()
        conn.close()


        st.session_state.entrenamiento = []


        st.success(
            "✅ Entrenamiento guardado correctamente"
        )



# ---------------------------------
# CERRAR SESIÓN
# ---------------------------------

st.divider()


if st.button("🔒 Cerrar sesión"):

    st.session_state.login = False
    st.session_state.entrenamiento = []

    st.rerun()