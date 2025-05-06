import pandas as pd
import streamlit as st
from utils import simulate_tour
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Elo Rating in Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load data ------------------------
matches_df = pd.read_csv('web/web_data/clean_atp_matches.csv')
players_df = pd.read_csv('web/web_data/clean_atp_players.csv')
assert matches_df.isna().sum().sum() == 0, f'nan values in matches\n{matches_df.isna().sum()}'
assert players_df.isna().sum().sum() == 0, f'nan values in players\n{players_df.isna().sum()}'

# Functions -------------------------
def values_changed():
    st.write('Values have changed. Click the "Run the simulation" button on the left sidebar to see the new results.')

# Sidebar ---------------------------
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Input K-factor', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer', on_change=values_changed)
    ksi = st.number_input('Input xi', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer', on_change=values_changed)
    s = st.selectbox('Input score type:', options=['delta', 'thirds'], index=0, on_change=values_changed)
    initial_elo = st.number_input('Initial Elo rating', min_value=0, max_value=5000, step=1, value=1500, placeholder='Enter a integer', on_change=values_changed)
    min_games = st.number_input('Min number of games to enter ranking', min_value=0, max_value=1000, step=1, value=30, placeholder='Enter a integer', on_change=values_changed)
    years = list(range(1970, 2025))
    # year_list = st.multiselect('Select the year you want to see:', options=years)

    run_simulation = st.button('Run simulation', key='run_simulation')

# Main page -------------------------

st.markdown("<h1 style='text-align: center; color: black;'>Elo Rating in Tennis</h1>", unsafe_allow_html=True)

if run_simulation:
    
    ranking, elo_history = simulate_tour(matches_df, players_df, k, ksi, s, initial_elo, min_games)

    # last_game_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    # ranking_filtered = ranking[ranking['last_game'] >= '2023-01-01']

    st.markdown("<h2 style='text-align: center; color: black;'>Ranking</h2>", unsafe_allow_html=True)
    st.write(ranking[
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

    st.divider() # ----------------------------------

    # Plots 
    st.markdown("<h2 style='text-align: center; color: black;'>Plots</h2>", unsafe_allow_html=True)

    # Histogram
    fig1, ax1 = plt.subplots()
    elos = ranking['Elo Rating'].tolist()
    ax1.hist(elos, bins=50)
    ax1.set_title('Elo Rating Distribution')
    ax1.set_xlabel('Elo Rating')
    ax1.set_ylabel('Frequency')
    st.pyplot(fig1)

    # Elo history
    fig2, ax2 = plt.subplots()
    ax2.set_title('Top 5 Players Elo History')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Elo Rating')

    top_five = ranking.nlargest(5, 'Elo Rating')['player_id'].tolist()
    top_five_elos = elo_history[elo_history['player_id'].isin(top_five)].sort_values(by=['date'])

    for player_id in top_five:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id]
        name = players_df.loc[players_df['player_id'] == player_id, 'First Name'].values[0]
        surname = players_df.loc[players_df['player_id'] == player_id, 'Last Name'].values[0]
        ax2.plot(player_elos['date'], player_elos['elo_rating'], label=f'{name} {surname}')

    ax2.legend()

    st.pyplot(fig2)
    
