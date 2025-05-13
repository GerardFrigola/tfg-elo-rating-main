import pandas as pd
import streamlit as st
from streamlit import session_state as ss
import utils as ut
from utils import simulate_tour, plot_elos_histogram
from datetime import datetime
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load data \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
matches_df = pd.read_csv('web_data/clean_atp_matches.csv')
players_df = pd.read_csv('web_data/clean_atp_players.csv')
initial_ranking = pd.read_csv('web_data/atp_initial_ranking.csv')
initial_elo_history = pd.read_csv('web_data/atp_initial_elo_history.csv')
assert matches_df.isna().sum().sum() == 0, f'nan values in matches\n{matches_df.isna().sum()}'
assert players_df.isna().sum().sum() == 0, f'nan values in players\n{players_df.isna().sum()}'
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Functions \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def values_changed():
    st.sidebar.markdown(':orange[El valor dels paràmetres ha canviat. Si us plau, torna a llançar la simulació per veure els resultats.]')
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Sidebar \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Paràmetre K', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer', on_change=values_changed, help='El paràmetre K controla la quantitat de canvi en el rànquing d\'un jugador després d\'una victòria o derrota. Un valor més alt significa que el rànquing canvia més ràpidament i que la distribució final de puntuacións serà més plana i ampla.')
    ksi = st.number_input('Paràmetre xi', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer', on_change=values_changed, help='Una diferència de <xi> punts entre dos jugadors significa que el jugador amb la puntuació més alta és deu vegades més probable que guanyi a l\'altre jugador. Un valor més alt significa que el rànquing és més sensible a les diferències de puntuació entre jugadors.')
    s = st.selectbox('Input score type:', options=['delta', 'thirds'], index=0, on_change=values_changed)
    initial_elo = st.number_input('Initial Elo rating', min_value=0, max_value=5000, step=1, value=1500, placeholder='Enter a integer', on_change=values_changed)
    min_games = st.number_input('Nombre mínim de partits jugats per entrar al ranquing', min_value=0, max_value=1000, step=1, value=30, placeholder='Enter a integer', on_change=values_changed)
    years = list(range(1970, 2025))
    # year_list = st.multiselect('Select the year you want to see:', options=years)

    run_simulation = st.button('Llença la simulació', type='primary')
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Session state: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
if 'atp_ranking' not in ss:
    ss['atp_ranking'] = initial_ranking

if 'atp_elo_history' not in ss:
    ss['atp_elo_history'] = initial_elo_history

if 'atp_start_year' not in ss:
    ss['atp_start_year'] = 1970

if 'atp_end_year' not in ss:
    ss['atp_end_year'] = 2024

if 'atp_selected_player_names' not in ss:
    names = ss['atp_ranking'].nlargest(5, 'Elo Rating')['First Name'].to_list()
    surnames = ss['atp_ranking'].nlargest(5, 'Elo Rating')['Last Name'].to_list()
    ss['atp_selected_player_names'] = [n + ' ' + s for n, s in zip(names, surnames)]
    

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    

#########################################################################################################################
# Main page #############################################################################################################

st.markdown("<h1 style='text-align: center; color: black;'>Elo Rating al Tennis</h1>", unsafe_allow_html=True)

if run_simulation:
    ss['atp_ranking'], ss['atp_elo_history'] = ut.simulate_tour(matches_df, players_df, k, ksi, s, initial_elo, min_games)

top_five = ss['atp_ranking'].nlargest(5, 'Elo Rating')
top_five_options = {
    name: player_id
    for name, player_id in zip(
        top_five['First Name'] + ' ' + top_five['Last Name'],
        top_five['player_id']
    )
}

player_dict_options = {
    name: player_id
    for name, player_id in zip(
        ss['atp_ranking']['First Name'] + ' ' + ss['atp_ranking']['Last Name'],
        ss['atp_ranking']['player_id']
    )
}

# RANKING:
st.markdown("<h2 style='text-align: center; color: black;'>Ranking</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
col1.write(ss['atp_ranking'][
    ['rank',
    'First Name', 
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
].set_index('rank'))

# Histogram
ut.plot_elos_histogram(ss['atp_ranking'], col2)

st.divider() # ------------------------------------------------------------------------------------------------------

# PLOTS:
st.markdown("<h2 style='text-align: center; color: black;'>Plots</h2>", unsafe_allow_html=True)

# Selection of players
ss['atp_selected_player_names'] = st.multiselect('Selecciona els jugadors que vols veure:', options=player_dict_options.keys(), default=top_five_options.keys(), key='year_list', max_selections=10)
selected_player_ids = [player_dict_options[key] for key in ss['atp_selected_player_names']]

# Selection of years
ss['atp_start_year'], ss['atp_end_year'] = st.select_slider(
    "Selecciona el rang dels anys que vols veure",
    options=list(range(1970, 2025)),
    value=(1970, 2024),
)

# Elo history along date
chart2 = ut.plot_elo_history_date_st(ss['atp_ranking'], ss['atp_elo_history'], selected_player_ids, ss['atp_start_year'], ss['atp_end_year'])
st.altair_chart(chart2, use_container_width=True)

# Elo history along n-games
chart3 = ut.plot_elo_history_ngames_st(ss['atp_ranking'], ss['atp_elo_history'], selected_player_ids)
st.altair_chart(chart3, use_container_width=True)

  
    
