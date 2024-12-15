#standard(stats)
stats = ["player","nationality","position","team","age","birth_year","games","games_starts","minutes","minutes_90s","goals","assists","goals_assists","goals_pens","pens_made","pens_att","cards_yellow","cards_red","xg","npxg","xg_assist","npxg_xg_assist","progressive_carries","progressive_passes","progressive_passes_received","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg_per90","xg_assist_per90","xg_xg_assist_per90","npxg_per90","npxg_xg_assist_per90"]
#shooting(shooting)
shooting = ["minutes_90s","goals","shots","shots_on_target","shots_on_target_pct","shots_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","average_shot_distance","shots_free_kicks","pens_made","pens_att","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
#passing(passing)
passing = ["passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xg_assist","pass_xa","xg_assist_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]
#passtypes(passing_types)
passing_types = ["passes_live","passes_dead","passes_free_kicks","through_balls","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_completed","passes_offsides","passes_blocked"]
#goal and shot creation(gca)
gca = ["sca","sca_per90","sca_passes_live","sca_passes_dead","sca_take_ons","sca_shots","sca_fouled", "sca_defense", "gca","gca_per90","gca_passes_live","gca_passes_dead","gca_take_ons","gca_shots","gca_fouled", "gca_defense"]
#defensive actions(defense)
defense = ["tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","challenges","challenge_tackles_pct","challenges_lost","blocks","blocked_shots","blocked_passes","interceptions","tackles_interceptions","clearances","errors"]
#possession(possession)
possession = ["touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","take_ons","take_ons_won","take_ons_won_pct","take_ons_tackled","take_ons_tackled_pct","carries","carries_distance","carries_progressive_distance"]
#miscallaneous(misc)
misc = ["cards_yellow","cards_red","cards_yellow_red","fouls","fouled","offsides","crosses","interceptions","tackles_won","pens_won","pens_conceded","own_goals","ball_recoveries","aerials_won","aerials_lost","aerials_won_pct"]

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import streamlit as st
import altair as alt
from common.menu import generarMenu

st.set_page_config(page_title="Análisis API", page_icon="📊", layout="wide")

generarMenu(st.session_state['usuario'])

st.image("pages/Premier.png")
st.title("Análisis de Datos con API")

#Las siguientes funciones extraen los datos en un dataframe

def get_tables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    player_table = all_tables[2]
    return player_table, team_table

def get_frame(features, player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all('tr')

    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
            for f in features_wanted_player:
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if(text == ''):
                    text = '0'
                if((f!='player')&(f!='nationality')&(f!='position')&(f!='team')&(f!='age')&(f!='birth_year')):
                    text = float(text.replace(',',''))
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player

def frame_for_category(category,top,end,features):
    url = (top + category + end)
    player_table, team_table = get_tables(url)
    df_player = get_frame(features, player_table)
    return df_player

def get_outfield_data(top, end):
    df1 = frame_for_category('stats', top, end, stats)
    df2 = frame_for_category('shooting', top, end, shooting)
    df3 = frame_for_category('passing', top, end, passing)
    df4 = frame_for_category('passing_types', top, end, passing_types)
    df5 = frame_for_category('gca', top, end, gca)
    df6 = frame_for_category('defense', top, end, defense)
    df7 = frame_for_category('possession', top, end, possession)
    df8 = frame_for_category('misc', top, end, misc)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df


@st.cache_data
def cargarDatos():
    df = get_outfield_data('https://fbref.com/en/comps/9/2023-2024/','/2023-2024-Premier-League-Stats')
    return df

df = cargarDatos()

# Estadísticas de Jugadores
st.header("Jugadores")

club = st.selectbox('Seleccione un Club', df['team'].unique())
#df=[df['team'] == club]
#df1 = df[~df['team'].isin([club])]
df1 = df.query('team == @club')

cols = st.columns(2)
cols[0].header("Plantilla")
cols[0].dataframe(df1, hide_index=True, )

cols[1].header("Gráfico de Edades")
# Agrupamos los datos en función de la columna 'ciudad'
df2 = df1.groupby(['team', 'age'])['age'].count().reset_index(name='count')

# Aolicamos la función 'mean' a la columna 'temperatura' para calcular el promedio


g = alt.Chart(df2).mark_bar().encode(x="age", y="count",)
cols[1].altair_chart(g, use_container_width=True)

