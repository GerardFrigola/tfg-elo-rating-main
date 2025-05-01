import pandas as pd
import streamlit as st
from entities import Player, Match, Tour
from utils import load_tour_from_csv, simulate_tour, save_ranking_to_df
from time import time, sleep
import os

st.set_page_config(
    page_title='Elo Rating in Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load data ------------------------
matches = pd.read_csv('web/web_data/clean_atp_matches.csv')
players = pd.read_csv('web/web_data/clean_atp_players.csv')
players_dic = {player_id: {
    'player_id': player_id, 
    'elo_rating': 0, 
    'elo_clay_rating': 0, 
    'elo_hard_rating': 0, 
    'elo_grass_rating': 0, 
    'elo_carpet_rating': 0, 
    'elo_unknown_rating': 0
    } for player_id in players['player_id']}


# Sidebar ---------------------------
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Input K-factor: (must be an integer)', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer')
    xi = st.number_input('Input xi: (must be a integer)', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer')
    s = st.selectbox('Select the type of simulation:', options=['delta', 'ratio'], index=0)

    years = list(range(1970, 2025))
    year_list = st.multiselect('Select the year you want to see:', options=years)

# Functions -------------------------
    
def simulate_tour(tour_df:pd.DataFrame, players:dict[str, dict[str:float]], k, ksi, s) -> None: 
    assert tour_df.isna().sum().sum() == 0, f'nan values in tour_df\n{tour_df.isna().sum()}'
    start = time()

    total_matches = len(tour_df)
    print(f'{total_matches} matches to simulate.\n')
    year = ''

    for _, m in tour_df.iterrows():
        if year != m['match_year']:
            print(f'    Simulating year {m['match_year']}...')
            year = m['match_year']

        # Update elo ratings
        Sw = 1
        Sl = 0

        # Algorisme per calcular elo-ratings
        winner_id = m['winner_id']
        loser_id = m['loser_id']
        surface = f'elo_{m['surface'].lower()}_rating'

        old_wr =  players[winner_id]['elo_rating']
        old_lr = players[loser_id]['elo_rating']
        # Surface
        old_slr = players[winner_id][surface]
        old_swr = players[loser_id][surface]

        mu_w = 1 / (1 + pow(10, -(old_wr - old_lr)/ksi))
        mu_l = 1 / (1 + pow(10, -(old_lr - old_wr)/ksi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -(old_swr - old_slr)/ksi))
        mu_sl = 1 / (1 + pow(10, -(old_slr - old_swr)/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors. 
        players[winner_id]['elo_rating'] = old_wr + k*(Sw - mu_w)
        players[loser_id]['elo_rating'] = old_lr + k*(Sl - mu_l)
        # Surface
        players[winner_id][surface] = old_swr + k*(Sw - mu_sw)
        players[loser_id][surface] = old_slr + k*(Sl - mu_sl)
        
        # TODO: Històric
        # winner.elo_history[tourney_date] = winner.elo_rating
        # loser.elo_history[tourney_date] = loser.elo_rating
        # # Surface
        # winner.elo_surf_history[surface][tourney_date] = winner.elo_surf_rating[surface]
        # loser.elo_surf_history[surface][tourney_date] = loser.elo_surf_rating[surface]
    
    end = time()
    print(f'Tour simulated. Time: {end-start:.2f}s {(end-start)/60:.2f}min\n')
    print(f'Saving results')

    # Save results
    return players



# Main page -------------------------
    
st.title('Elo Rating in Tennis')
st.subheader('Matches')
if not year_list:
    st.write(matches)
else:
    st.write(matches[matches['match_year'].isin(year_list)])


if st.button('Run simulation'):  

    players_simulated_dic = simulate_tour(matches, players_dic, k=24, ksi=400, s='delta')

    players_simulated = pd.DataFrame.from_dict(players_simulated_dic, orient='index')

    players = players.merge(players_simulated, how='left', on='player_id')\
        .sort_values(by='elo_rating', ascending=False)
    
st.write(players)


