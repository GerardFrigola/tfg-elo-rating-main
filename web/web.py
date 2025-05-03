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
assert matches.isna().sum().sum() == 0, f'nan values in matches\n{matches.isna().sum()}'
assert players.isna().sum().sum() == 0, f'nan values in players\n{players.isna().sum()}'

# Functions -------------------------
    
def simulate_tour(tour_df:pd.DataFrame, k, ksi, s, initial_elo): 
    assert tour_df.isna().sum().sum() == 0, f'nan values in tour_df\n{tour_df.isna().sum()}'

    players_dic = {player_id: {
    'player_id': player_id, 
    'elo_rating': initial_elo, 
    'elo_clay_rating': initial_elo, 
    'elo_hard_rating': initial_elo, 
    'elo_grass_rating': initial_elo, 
    'elo_carpet_rating': initial_elo, 
    'elo_unknown_rating': initial_elo
    } for player_id in players['player_id']}

    placeholder = st.empty()
    start = time()

    total_matches = len(tour_df)

    placeholder.write(f'Simulating {total_matches} matches...')
    year = ''
    for _, m in tour_df.iterrows():
        
        if year != m['match_year']:
            # placeholder.write(f'    Simulating year {m['match_year']}...')
            year = m['match_year']

        # Update elo ratings
        match s:
            case 'delta':
                Sw = 1
                Sl = 0
            case 'thirds': 
                if m['best_of'] != m['num_sets'] or m['best_of'] == 1:
                    Sw = 1
                    Sl = 0
                else: 
                    Sw = 2/3
                    Sl = 1/3

        # Algorisme per calcular elo-ratings
        winner_id = m['winner_id']
        loser_id = m['loser_id']
        surface = f'elo_{m['surface'].lower()}_rating'

        old_wr =  players_dic[winner_id]['elo_rating']
        old_lr = players_dic[loser_id]['elo_rating']
        # Surface
        old_slr = players_dic[winner_id][surface]
        old_swr = players_dic[loser_id][surface]

        mu_w = 1 / (1 + pow(10, -(old_wr - old_lr)/ksi))
        mu_l = 1 / (1 + pow(10, -(old_lr - old_wr)/ksi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -(old_swr - old_slr)/ksi))
        mu_sl = 1 / (1 + pow(10, -(old_slr - old_swr)/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors. 
        players_dic[winner_id]['elo_rating'] = old_wr + k*(Sw - mu_w)
        players_dic[loser_id]['elo_rating'] = old_lr + k*(Sl - mu_l)
        # Surface
        players_dic[winner_id][surface] = old_swr + k*(Sw - mu_sw)
        players_dic[loser_id][surface] = old_slr + k*(Sl - mu_sl)

        # TODO: Històric
        # winner.elo_history[tourney_date] = winner.elo_rating
        # loser.elo_history[tourney_date] = loser.elo_rating
        # # Surface
        # winner.elo_surf_history[surface][tourney_date] = winner.elo_surf_rating[surface]
        # loser.elo_surf_history[surface][tourney_date] = loser.elo_surf_rating[surface]

    placeholder.empty()
    end = time()

    players_simulated: pd.DataFrame = pd.DataFrame.from_dict(players_dic, orient='index')

    ranking: pd.DataFrame = players.merge(players_simulated, how='left', on='player_id')\
        .sort_values(by='elo_rating', ascending=False)\
        .reset_index(drop=True)\
        .drop(columns=['elo_unknown_rating'])\
        .rename(columns={
            'elo_rating': 'Elo Rating', 
            'elo_clay_rating': 'Clay Elo Rating', 
            'elo_hard_rating': 'Hard Elo Rating', 
            'elo_grass_rating': 'Grass Elo Rating', 
            'elo_carpet_rating': 'Carpet Elo Rating'
        })
    
    ranking.index += 1

    return ranking

def values_changed():
    st.write('Values have changed. Rerun the simulation to see the new results.')

# Sidebar ---------------------------
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Input K-factor', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer', on_change=values_changed)
    ksi = st.number_input('Input xi', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer', on_change=values_changed)
    s = st.selectbox('Input score type:', options=['delta', 'thirds'], index=0, on_change=values_changed)
    show_surfaces = st.checkbox('Show surface ratings', value=False)
    initial_elo = st.number_input('Initial Elo rating', min_value=0, max_value=5000, step=1, value=1500, placeholder='Enter a integer', on_change=values_changed)

    years = list(range(1970, 2025))
    # year_list = st.multiselect('Select the year you want to see:', options=years)

    run_simulation = st.button('Run simulation', key='run_simulation')




# Main page -------------------------
    
st.title('Elo Rating in Tennis')
st.subheader('Ranking')

if run_simulation:
    ranking = simulate_tour(matches, k, ksi, s, initial_elo)

    if show_surfaces:
        st.write(ranking)
    else:
        st.write(ranking[['First Name', 'Last Name', 'Elo Rating', 'Hand', 'Country', 'Height', 'player_id']])

st.divider() # ----------------------------------


# if not year_list:
#     st.write(matches)
# else:
#     st.write(matches[matches['match_year'].isin(year_list)])

