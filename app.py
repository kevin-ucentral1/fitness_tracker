

import streamlit as st

# prueba de conexión a secrets
#st.write(st.secrets["postgres"]["host"])


# tu aplicación actual
st.title("Fitness Tracker")


import streamlit as st
from database import conectar
import streamlit as st
from database import conectar


st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏋️"
)


st.title("🏋️ Fitness Tracker")


# Memoria temporal de la sesión
if "entrenamiento" not in st.session_state:
    st.session_state.entrenamiento = []


st.subheader("Registrar entrenamiento")


# Datos del ejercicio

ejercicio = st.text_input(
    "Ejercicio"
)


peso = st.number_input(
    "Peso utilizado (kg)",
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


# Agregar ejercicio a la sesión

if st.button("➕ Agregar ejercicio"):

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



# Mostrar ejercicios actuales

st.divider()

st.subheader("📋 Entrenamiento actual")


if len(st.session_state.entrenamiento) == 0:

    st.info(
        "Todavía no has agregado ejercicios"
    )

else:

    for i, e in enumerate(
        st.session_state.entrenamiento,
        start=1
    ):

        st.write(
            f"""
            {i}. **{e['ejercicio']}**
            
            Peso: {e['peso']} kg  
            Series: {e['series']}  
            Repeticiones: {e['repeticiones']}
            """
        )



# Guardar todo en Supabase

st.divider()


if st.button("💾 Finalizar entrenamiento"):


    if len(st.session_state.entrenamiento) == 0:

        st.warning(
            "No hay ejercicios para guardar"
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


        # limpiar entrenamiento actual

        st.session_state.entrenamiento = []


        st.success(
            "✅ Entrenamiento guardado correctamente"
        )