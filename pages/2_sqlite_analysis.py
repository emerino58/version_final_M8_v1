import streamlit as st
import altair as alt
import sqlite3
import pandas as pd
from common.menu import generarMenu
import matplotlib.pyplot as plt
import numpy as np
from plotly.graph_objects import Figure, Indicator
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image, ImageEnhance
import io
import base64
import mpld3

# st.set_page_config(page_title="Análisis SQLite", page_icon="📊", layout="wide")

# generarMenu(st.session_state['usuario'])

##############################################################################
# Función para agregar un fondo degradado transparente
def agregar_fondo(imagen_path):
    img = Image.open(imagen_path)

    # Ajustar tonos azulados y brillo
    enhancer = ImageEnhance.Color(img)
    img_azulado = enhancer.enhance(0.5)
    enhancer_brightness = ImageEnhance.Brightness(img_azulado)
    img_azulado = enhancer_brightness.enhance(0.7)

    # Convertir la imagen a un formato base64
    buffer = io.BytesIO()
    img_azulado.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode()

    # Estilo CSS para el fondo, bordes y selectores
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 0.85;
        filter: brightness(0.95);
    }}
    .stAltairChart, .stPlotlyChart, .stPyplot {{
        border: 3px solid black; /* Contorno negro de 3 puntos */
        border-radius: 5px; /* Bordes redondeados opcionales */
        padding: 10px; /* Espaciado interno */
    }}
    .stDataFrame {{
        border: 3px solid black;
    }}
    .stSelectbox {{
        border: 3px solid black;
        border-radius: 5px;
        padding: 5px;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Agregar fondo azul degradado transparente usando la función
agregar_fondo("Fondo.png")

#generarMenu(st.session_state['usuario'])
###############################################################################



st.image("pages\Itau_Black.png")
st.title("⚽ Estadísticas de Jugadores")

# Conexión a la base de datos
conn = sqlite3.connect('data/chile.db')

# Estadísticas de Jugadores
st.header("Jugadores")

# Seleccionar un Club
#club = "Audax Italiano"
df_team4 = pd.read_sql_query("SELECT DISTINCT equipo FROM jugadores ORDER BY equipo", conn)
club = st.selectbox('Seleccione un Club', df_team4['equipo'])
df_team4 = pd.read_sql_query("SELECT DISTINCT edad FROM jugadores ORDER BY edad", conn)
edad = st.selectbox('Seleccione una Edad', df_team4['edad'])
df_team5 = pd.read_sql_query("SELECT * FROM jugadores WHERE equipo = ? AND edad = ?", conn, params = [club, edad])

cols5 = st.columns(2)
df_team6 = pd.read_sql_query("SELECT * FROM jugadores WHERE equipo = ? ", conn, params = [club])
cols5[0].dataframe(df_team5, hide_index=True, )

cols5[1].header("Gráfico de Edades")
df_team7 = pd.read_sql_query("SELECT equipo, edad, count('edad') AS cantidad FROM jugadores WHERE equipo = ? GROUP BY edad", conn, params = [club])
cols5[1].bar_chart(df_team7.set_index('edad')['cantidad'], x_label=[club], y_label="Cantidad")

cols6 = st.columns(2)
cols6[0].header("Gráfico de Puestos")
df_team8 = pd.read_sql_query("SELECT equipo, posicion, count('posicion') AS cantidad FROM jugadores WHERE equipo = ? GROUP BY posicion", conn, params = [club])
cols6[0].bar_chart(df_team8.set_index('posicion')['cantidad'], x_label=[club], y_label="Cantidad")

cols6[1].header("Gráfico de Nacionalidades")
df_team8 = pd.read_sql_query("SELECT equipo, nacionalidad, count('nacionalidad') AS cantidad FROM jugadores WHERE equipo = ? GROUP BY nacionalidad", conn, params = [club])
a = alt.Chart(df_team8).mark_arc().encode(theta="cantidad", color="nacionalidad")

cols6[1].altair_chart(a, use_container_width=True)

jugador = st.selectbox('Seleccione un Jugador', df_team6['jugador'])
df_team9 = pd.read_sql_query("SELECT * FROM jugadores WHERE jugador = ?", conn, params = [jugador])
cols7 = st.columns(2)
cols7[0].dataframe(df_team9, hide_index=True, use_container_width = True)
df_team10 = pd.read_sql_query("SELECT logo FROM posiciones INNER JOIN jugadores ON posiciones.club = jugadores.equipo WHERE jugadores.equipo = ? AND jugadores.jugador = ?", conn, params = [club, jugador])
path = df_team10['logo'].astype(str).to_string(index=False)
cols7[1].image(path, caption=[club], output_format = "auto")

cols8 = st.columns(2)
cols8[0].header("Gráfico de Métricas")

# Grafico de Barras Radial

# Valores para Grafico y las columnas relevantes
df_graf = df_team9[[
    'portirpor', 'porgolhec', 'porprecen', 
    'porprepas', 'porprepasad', 'porprepasat', 
    'porprepaslat', 'porprepasco', 'porprepaslar'
]]

# Valores del DataFrame para 2024
valores = df_graf.iloc[0].values

# Etiquetas para cada métrica
labels = [
    'Tiros a Porteria', 'Goles Hechos', 'Precisión de Centros', 
    'Precisión de Pases', 'Precisión de Pases Adelante', 'Precisión de Pases Atrás', 
    'Precisión de Pases Laterales', 'Presición de Pases C/M', 'Presición de Pases Largos'
]

# Número de variables
num_vars = len(labels)

# Colores de las barras (puedes ajustarlos como prefieras)
colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#FF6347', '#4682B4', '#32CD32', '#FFD700', '#FF6347']

# Crear ángulos para las barras
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

# Crear el gráfico polar (radial) con barras más anchas y valores dentro de las barras
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Dibujar las barras con mayor ancho (width=0.4)
bars = ax.bar(angles, valores, width=0.4, bottom=0, color=colors, edgecolor='black', alpha=0.7)

# Añadir etiquetas en los ángulos
ax.set_xticks(angles)
ax.set_xticklabels(labels)

# Añadir título al gráfico
ax.set_title(jugador, size=16, pad=20)

# Añadir los valores dentro de cada barra (centrados en el gajo)
for bar, value, angle in zip(bars, valores, angles):
    ax.text(angle, bar.get_height() / 2, f'{value:.1f}', ha='center', va='center', fontsize=10, color='black')
cols8[0].pyplot(plt.gcf(), use_container_width=True)

cols8[1].header("Gráfico de Participación")

# Filtrar el rendimiento del club seleccionado
participacion_jug = (df_team9['minutosj'].values[0] / 2850) * 100

# Crear el velocímetro (gauge)
fig = Figure()

fig.add_trace(Indicator(
    mode="gauge+number",
    value=participacion_jug,  # Convertir a porcentaje
    title={"text": f"Participación de {jugador}"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, 50], "color": "red"},
            {"range": [50, 75], "color": "yellow"},
            {"range": [75, 100], "color": "green"}
        ],
    }
))

# Mostrar el velocímetro
cols8[1].plotly_chart(fig)

# Botón para retroceder página
btnAnterior = st.button("Anterior")
if btnAnterior:
    st.switch_page('pages/sqlite_analysis.py')