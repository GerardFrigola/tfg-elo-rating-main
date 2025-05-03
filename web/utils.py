import pandas as pd
import streamlit as st
from time import time

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
