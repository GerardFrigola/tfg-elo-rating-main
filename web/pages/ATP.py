import pandas as pd
import streamlit as st
from streamlit import session_state as ss
import utils as ut
from utils import simulate_tour, plot_elos_histogram
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load data ------------------------
matches_df = pd.read_csv('web/web_data/clean_atp_matches.csv')
players_df = pd.read_csv('web/web_data/clean_atp_players.csv')
initial_ranking = pd.read_csv('web/web_data/initial_ranking.csv')
initial_elo_history = pd.read_csv('web/web_data/initial_elo_history.csv')
assert matches_df.isna().sum().sum() == 0, f'nan values in matches\n{matches_df.isna().sum()}'
assert players_df.isna().sum().sum() == 0, f'nan values in players\n{players_df.isna().sum()}'

# Functions -------------------------
def values_changed():
    st.sidebar.markdown(':orange[El valor dels paràmetres ha canviat. Si us plau, torna a llançar la simulació per veure els resultats.]')



# Sidebar ---------------------------
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Paràmetre K', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer', on_change=values_changed, help='El paràmetre K controla la quantitat de canvi en el rànquing d\'un jugador després d\'una victòria o derrota. Un valor més alt significa que el rànquing canvia més ràpidament i que la distribució final de puntuacións serà més plana i ampla.')
    ksi = st.number_input('Paràmetre xi', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer', on_change=values_changed, help='Una diferència de <xi> punts entre dos jugadors significa que el jugador amb la puntuació més alta és deu vegades més probable que guanyi a l\'altre jugador. Un valor més alt significa que el rànquing és més sensible a les diferències de puntuació entre jugadors.')
    s = st.selectbox('Input score type:', options=['delta', 'thirds'], index=0, on_change=values_changed)
    initial_elo = st.number_input('Initial Elo rating', min_value=0, max_value=5000, step=1, value=1500, placeholder='Enter a integer', on_change=values_changed)
    min_games = st.number_input('Min number of games to enter ranking', min_value=0, max_value=1000, step=1, value=30, placeholder='Enter a integer', on_change=values_changed)
    years = list(range(1970, 2025))
    # year_list = st.multiselect('Select the year you want to see:', options=years)

    run_simulation = st.button('Llença la simulació', type='primary')


# Session state: --------------------
if 'ranking' not in ss:
    ss.ranking = initial_ranking

if 'elo_history' not in ss:
    ss.elo_history = initial_elo_history


# Main page -------------------------

st.markdown("<h1 style='text-align: center; color: black;'>Elo Rating al Tennis</h1>", unsafe_allow_html=True)

if run_simulation:
    ss.ranking, ss.elo_history = ut.simulate_tour(matches_df, players_df, k, ksi, s, initial_elo, min_games)

st.markdown("<h2 style='text-align: center; color: black;'>Ranking</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
col1.write(ss.ranking[
    ['First Name', 
    'Last Name', 
    'Elo Rating', 
    'Hand',
    'Country', 
    'Height', 
    'Clay Elo Rating', 
    'Hard Elo Rating', 
    'Grass Elo Rating', 
    'Carpet Elo Rating', 
    'player_id',
    'last_game',
    'n_games']
])

# Histogram
ut.plot_elos_histogram(ss.ranking, col2)

st.divider() # ----------------------------------

# PLOTS
st.markdown("<h2 style='text-align: center; color: black;'>Plots</h2>", unsafe_allow_html=True)

# Elo history along date
ut.plot_elo_history_date(ss.ranking, ss.elo_history)

# Elo history along n-games
ut.plot_elo_history_ngames(ss.ranking, ss.elo_history)

# Elo history along surface
ut.plot_elo_history_surface(ss.ranking, ss.elo_history, 104745)
  
    
