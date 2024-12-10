import streamlit as st
import models.sqlite as db

def generarMenu(usuario):
    """Genera el menú dependiendo del usuario

    Args:
        usuario (str): usuario utilizado para generar el menú
    """
    with st.sidebar:
        # Consultar la base de datos SQLite para obtener el nombre del usuario
        query = "SELECT nombre FROM usuarios WHERE usuario = ?"
        params = (usuario,)
        result = db.execute_query(query, params)

        # Verificar si se encontró el usuario
        if result:
            nombre = result[0][0]  # Tomar el nombre del resultado de la consulta
            # Mostrar el nombre del usuario
            st.write(f"Hola **:blue-background[{nombre}]** ")
        else:
            st.error("Usuario no encontrado en la base de datos.")

        # Mostrar los enlaces de páginas
        st.page_link("home.py", label="Home", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/sqlite_analysis.py", label="Liga Chilena (SQLite)", icon=":material/sell:")
        st.page_link("pages/API_analysis.py", label="Liga Inglesa (API)", icon=":material/shopping_cart:")

        # Botón para cerrar la sesión
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun()
