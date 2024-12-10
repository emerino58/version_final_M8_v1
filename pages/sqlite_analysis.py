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


st.set_page_config(page_title="Análisis SQLite", page_icon="📊", layout="wide")

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

generarMenu(st.session_state['usuario'])

# Título principal
st.markdown("<h1 style='color: yellow; font-weight: bold;'>📊 Panorámica Campeonato Itau 2024</h1>", unsafe_allow_html=True)

# Conexión a la base de datos
conn = sqlite3.connect('data/chile.db')

#######################################################
#######################################################

cols = st.columns(2)
cols[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Estadísticas de Equipos</h2>", unsafe_allow_html=True)
df_team = pd.read_sql_query("SELECT * FROM posiciones ORDER BY posicion", conn)
cols[0].dataframe(df_team, hide_index=True, column_order=("posicion", "club", "puntos", "puntose", "partidosj", "rendimiento", "partidosg", "partidose", "partidosp", "golesf", "golesc", "diferencia"))

#######################################
# Gráfico de Puntajes (Altair)
#######################################
cols[1].markdown("<h2 style='color: yellow; font-weight: bold;'>Gráfico de Puntajes</h2>", unsafe_allow_html=True)

# Configurar el gráfico
chart = alt.Chart(df_team).mark_bar(stroke='black', strokeWidth=3).encode(  # Contorno negro en barras
    x=alt.X('club', axis=alt.Axis(title="Clubes")),
    y=alt.Y('puntos', axis=alt.Axis(title="Puntaje"), scale=alt.Scale(domain=[0, 90]))  # Escala con rango de 0 a 90
).properties(
    #title=alt.TitleParams("Gráfico de Puntajes", color="black", fontSize=18, fontWeight="bold"),  # Título del gráfico
    width=640,  # Reducido en un 20%
    height=400  # Mantener la altura
)

# Mostrar el gráfico
cols[1].altair_chart(chart, use_container_width=False)  # No usar contenedor automático para respetar dimensiones

# Cerrar el contenedor
cols[1].markdown("</div>", unsafe_allow_html=True)

#########################################################
#########################################################



###########################################
# Gráfico de Posesión (Altair)
###########################################
cols2 = st.columns(2)
cols2[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Gráfico de Posesión</h2>", unsafe_allow_html=True)
df_team2 = pd.read_sql_query("SELECT equipos.club, posiciones.puntos, equipos.posesion FROM equipos INNER JOIN posiciones ON posiciones.club = equipos.club", conn)
g = alt.Chart(df_team2).mark_circle(stroke='black', strokeWidth=3).encode(  # Contorno negro en puntos
    x="puntos",
    y="posesion",
    color="club",
    size="puntos"
).properties(
    # title=alt.TitleParams("Gráfico de Posesión", color="yellow", fontSize=18, fontWeight="bold")
)
cols2[0].altair_chart(g, use_container_width=True)

#########################################
# Gráfico de  Goles (Altair)
#########################################
cols2[1].markdown("<h2 style='color: yellow; font-weight: bold;'>Gráfico de Goles</h2>", unsafe_allow_html=True)

# Gráfico de línea
line = alt.Chart(df_team).mark_line(color='blue').encode(
    x=alt.X('club', axis=alt.Axis(title="Club")),
    y=alt.Y(
        'puntos', 
        axis=alt.Axis(title="Puntaje y Goles"),
        scale=alt.Scale(domain=[0, 90])  # Ajustar rango del eje y
    )
)

# Puntos interactivos
points = alt.Chart(df_team).mark_point(color='red', size=60).encode(
    x=alt.X('club'),
    y=alt.Y('puntos'),
    tooltip=['club', 'puntos']  # Mostrar información al pasar el ratón
)

# Combinar línea y puntos
chart = (line + points).properties(
    height=380,  # Altura aumentada para 2 cm adicionales
    width=600    # Mantener el ancho para proporción visual
)

# Mostrar el gráfico
cols2[1].altair_chart(chart, use_container_width=False)
###########################################
# Gráfico de Métricas (Matplotlib)
###########################################
#club = st.selectbox('Seleccione un Club', df_team['club'], key="selectbox_club")
#df_team3 = pd.read_sql_query("SELECT logo, rendimiento FROM posiciones WHERE club = ?", conn, params=[club])

# Validar que el resultado de la consulta no esté vacío
#if not df_team3.empty:
#    rendimiento_club = df_team3['rendimiento'].iloc[0]  # Obtener el valor de rendimiento
#    path = df_team3['logo'].iloc[0]  # Obtener el path del logo
#else:
#    rendimiento_club = 0  # Valor por defecto si no hay datos
#    path = None  # No se muestra logo si no hay datos

#cols3 = st.columns(2)

#cols3[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Indicadores de Equipos</h2>", unsafe_allow_html=True)
#df_team2 = pd.read_sql_query("SELECT * FROM metricas WHERE club = ?", conn, params=[club])
#cols3[0].dataframe(df_team2, hide_index=True, use_container_width=True)

#if path:
#    cols3[1].image(path, caption=[club], output_format="auto")
#else:
#    cols3[1].markdown("<p style='color: red;'>No hay logo disponible para este club.</p>", unsafe_allow_html=True)

cols4 = st.columns(2)
cols4[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Seleccione un Club</h2>", unsafe_allow_html=True)


#################################################################################
#################################################################################
club = st.selectbox('Club', df_team['club'])
df_team3 = pd.read_sql_query("SELECT logo, rendimiento FROM posiciones WHERE club = ?", conn, params = [club])
cols3 = st.columns(2)

cols3[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Indicadores del  Equipo</h2>", unsafe_allow_html=True)    ## header("Indicadores de Equipos")
df_team2 = pd.read_sql_query("SELECT * FROM metricas WHERE club = ?", conn, params = [club])
cols3[0].dataframe(df_team2, hide_index=True, use_container_width = True)
path = df_team3['logo'].astype(str).to_string(index=False)
cols3[1].image(path, caption=[club], output_format = "auto")

cols4 = st.columns(2)
cols4[0].markdown("<h2 style='color: yellow; font-weight: bold;'>Métricas del Equipo</h2>", unsafe_allow_html=True)    ## header("Indicadores de Equipos")
#######################################################################################
# Gráfico de Barras Radial
#######################################################################################
# Valores para Gráfico y las columnas relevantes
df_graf = df_team2[[
    'portirpor', 'porgolhec', 'porprecen', 
    'porprepas', 'porprepasad', 'porprepasat', 
    'porprepaslat', 'porprepaslar'
]]

# Valores del DataFrame para 2024
valores = df_graf.iloc[0].values

# Etiquetas para cada métrica
labels = [
    'Tiros a Porteria', 'Goles Hechos', 'Precisión de Centros', 
    'Precisión de Pases', 'Precisión de Pases Adelante', 'Precisión de Pases Atrás', 
    'Precisión de Pases Laterales', 'Presición de Pases Largos'
]

# Número de variables
num_vars = len(labels)

# Colores de las barras (puedes ajustarlos como prefieras)
colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#FF6347', '#4682B4', '#32CD32', '#FFD700']

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
ax.set_title(club, size=16, pad=20)

# Añadir los valores dentro de cada barra (centrados en el gajo)
for bar, value, angle in zip(bars, valores, angles):
    ax.text(angle, bar.get_height() / 2, f'{value:.1f}', ha='center', va='center', fontsize=10, color='black')
cols4[0].pyplot(plt.gcf(), use_container_width=True)

#cols4[1].header("Rendimiento")
cols4[1].markdown("<h2 style='color: yellow; font-weight: bold;'>Rendimiento del Equipo</h2>", unsafe_allow_html=True)    ## header("Indicadores de Equipos")
# title={
#    "text": f"<span style='color:yellow;'>Rendimiento de {club}</span>",  # Texto en amarillo
#    "font": {"size": 20, "family": "Arial Black"}  # Opciones adicionales de fuente
#}

# Filtrar el rendimiento del club seleccionado
rendimiento_club = df_team3['rendimiento'].values[0]

# Crear el velocímetro (gauge)
fig = Figure()

fig.add_trace(Indicator(
    mode="gauge+number",
    value=rendimiento_club,  # Convertir a porcentaje
    # title={"text": f"<span style='color:yellow;'>Rendimiento de {club}</span>", "font": {"size": 20, "family": "Arial Black"}},
    #
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
cols4[1].plotly_chart(fig)

conn.close()

##########################################################################
##########################################################################

# Comparativa de equipos
st.markdown("<h1 style='color: yellow; font-weight: bold;'>Comparativa de Equipos</h1>", unsafe_allow_html=True)
@st.cache_data
def cargar_datos():
    file_path = './data/NW_Puntaje.xlsx'
    return pd.read_excel(file_path)

puntaje_df = cargar_datos()
columnas_necesarias = ['Equipo'] + [f'Fecha_{i}' for i in range(1, 31)]
equipos_df = puntaje_df[columnas_necesarias]
equipos = list(equipos_df['Equipo'])

# Definir columnas antes de usarlas
col1, col2 = st.columns(2)

# Agregar estilos personalizados para los valores seleccionados
st.markdown("""
    <style>
    .stSelectbox div[role="combobox"] > div:first-child {
        color: black !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Selectores con rótulos en amarillo y valores en negro y negrita
with col1:
    col1.markdown("<span style='color: yellow; font-weight: bold;'>Equipo A</span>", unsafe_allow_html=True)  # Título en amarillo y negrita
    equipo_a = st.selectbox("", equipos, key="selectbox_equipo_a")  # Campo con key único

with col2:
    col2.markdown("<span style='color: yellow; font-weight: bold;'>Equipo B</span>", unsafe_allow_html=True)  # Título en amarillo y negrita
    equipo_b = st.selectbox("", equipos, key="selectbox_equipo_b")  # Campo con key único

container = st.container()
def comparar_equipos(equipo_a, equipo_b):
    if equipo_a not in equipos or equipo_b not in equipos:
        st.error("Uno o ambos equipos no están en la lista de datos.")
        return None, None
    datos_equipo_a = equipos_df[equipos_df['Equipo'] == equipo_a].iloc[:, 1:].values.flatten()
    datos_equipo_b = equipos_df[equipos_df['Equipo'] == equipo_b].iloc[:, 1:].values.flatten()
    return datos_equipo_a, datos_equipo_b

puntajes_a, puntajes_b = comparar_equipos(equipo_a, equipo_b)
if puntajes_a is not None and puntajes_b is not None:
    fechas = [f'Fecha_{i}' for i in range(1, 31)]
#    container.markdown("<h2 style='color: yellow; font-weight: bold;'>Comparativa de Rendimientos</h2>", unsafe_allow_html=True)
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, puntajes_a, label=f'{equipo_a}', marker='o')
    plt.plot(fechas, puntajes_b, label=f'{equipo_b}', marker='o')
    plt.title("Progresión de Puntajes", color="black", fontsize=18, fontweight="bold")
    plt.xlabel("Fechas")
    plt.ylabel("Puntaje")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    container.pyplot(plt)

# Botón para avanzar a la siguiente página
st.markdown("""
    <style>
    .stButton > button {
        background-color: red;
        color: white;
        font-size: 16px;
        border: 2px solid black;
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

btnAvanzar = st.button("Siguiente")
if btnAvanzar:
    st.switch_page("pages/2_sqlite_analysis.py")