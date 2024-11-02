import json
import pandas as pd
import streamlit as st
from mplsoccer import VerticalPitch

# Título de la aplicación
st.title("CL 2024 Shot Map")
st.subheader("Filtra por equipo/jugador para ver todos los disparos realizados.")

# Cargar los datos desde el CSV actualizado
df = pd.read_csv('df_shots_CL24.csv')

# Filtrar solo los eventos de disparo ("Shot") usando el nombre del evento
df = df[df['event_type_name'] == 'Shot'].reset_index(drop=True)

# Función para filtrar datos
def filter_data(df, team, player):
    if team:
        df = df[df['team_name'] == team]
    if player:
        df = df[df['player_name'] == player]
    return df

# Filtrado interactivo para equipo y jugador
team = st.selectbox("Selecciona un equipo", df['team_name'].sort_values().unique(), index=None)
player = st.selectbox("Selecciona un jugador", df[df['team_name'] == team]['player_name'].sort_values().unique(), index=None)

# Filtrar los datos según la selección
filtered_df = filter_data(df, team, player)

# Dibujar el campo de fútbol usando mplsoccer
pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Función para graficar los disparos
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location_x']),
            y=float(x['location_y']),
            ax=ax,
            s=1000 * x.get('statsbomb_xg', 0.1),  # Tamaño basado en la columna de xG si está disponible
            color='green' if x['outcome_name'] == 'Goal' else 'white',  # Color según si fue gol o no
            edgecolors='black',
            alpha=1 if x['outcome_name'] == 'Goal' else .5,
            zorder=2 if x['outcome_name'] == 'Goal' else 1
        )

# Graficar los disparos filtrados
plot_shots(filtered_df, ax, pitch)

# Mostrar la figura en Streamlit
st.pyplot(fig)
