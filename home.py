import streamlit as st
import base64  # Importar base64 para manejar la conversión de imágenes
import common.login as login

# Función para establecer la imagen de fondo con ajuste superior completo
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    b64_image = base64.b64encode(image_data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(
                rgba(255, 255, 255, 0.8), /* Blanco con opacidad del 80% */
                rgba(255, 255, 255, 0.8)
            ), 
            url("data:image/jpg;base64,{b64_image}");
            background-size: cover;
            background-position: top; /* Prioriza la parte superior de la imagen */
            background-attachment: fixed;
        }}
        h1 {{
            color: black; /* Cambiar el color del título a negro */
            font-size: 3rem;
            text-align: center;
            margin-top: 20px;
        }}
        .login-box {{
            # border: 5px solid black; /* Borde negro grueso */
            # border-radius: 10px; /* Bordes redondeados */
            # padding: 20px; /* Espaciado interno */
            # background-color: rgba(255, 255, 255, 0.9); /* Fondo blanco translúcido */
            # box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3); /* Sombra para efecto */
            max-width: 400px; /* Limitar el ancho máximo */
            margin: 20px auto; /* Centrar horizontalmente */
            position: relative; /* Asegura que no haya espacios superiores */
            top: -10px; /* Ajustar si hay margen adicional */
        }}
        label {{
            color: black; /* Color negro para las etiquetas */
            font-weight: bold; /* Negrita */
            font-size: 1.2rem;
        }}
        .stTextInput > div > div {{
            border: 4px solid black; /* Borde negro para los campos de entrada */
            border-radius: 5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Llama a la función para establecer el fondo
set_background_image("Modulo_8.jpg")

# Contenido de la aplicación
# st.markdown("<h1>MÓDULO 8</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color: black; font-weight: bold; font-size: 500%;'>MÓDULO 8</h1>", unsafe_allow_html=True)
# Crear un contenedor para el formulario de login y evitar espacios no deseados
with st.container():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    login.generarLogin()  # Generar el login directamente dentro del contenedor
    st.markdown('</div>', unsafe_allow_html=True)

if 'usuario' in st.session_state:
    st.markdown("### Creación de una Aplicación Interactiva con Streamlit", unsafe_allow_html=True)
    st.write('')
st.markdown("<h2 style='font-weight: bold; font-size: 120%;'>Objetivo:</h2>", unsafe_allow_html=True)
st.write('Aplicar los conocimientos adquiridos sobre desarrollo de aplicaciones web utilizando Streamlit para crear una aplicación interactiva que conecte múltiples fuentes de datos, con funcionalidades avanzadas como gestión de sesiones y cache.')
st.write('')
#st.write('Análisis de datos con SQLite y API')
st.markdown("<h2 style='font-weight: bold; font-size: 120%;'>Análisis de datos con SQLite y API</h2>", unsafe_allow_html=True)