import os
import sys
import pandas as pd
import numpy as np 
import streamlit as st
import argparse 
from time import time

from entities import Match, Player, Tour
from utils import load_tour_from_csv, load_tour_from_csv_parallel,  simulate_tour, save_ranking_to_df


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-k', required=True)
    # parser.add_argument('-xi', required=True)
    # args = parser.parse_args()

    # k = args.k
    # xi = args.xi
    
    print('Loading all matches...')

    initial_elo_rating = 0

    all_matches = pd.read_csv('modeling/data/clean_atp_matches.csv')
    players = pd.read_csv('modeling/data/clean_atp_players.csv')

    # Create the dictionary
    start = time()
    players_dic = {player_id: {'player_id': player_id, 'elo_rating': 0, 'elo_clay_rating': 0, 'elo_hard_rating': 0, 'elo_grass_rating': 0, 'elo_carpet_rating': 0, 'elo_unknown_rating': 0} for player_id in players['player_id']}
    print(f"Time to create players_dic: {time() - start:.2f} seconds")

    # players['elo_rating'] = pd.Series(initial_elo_rating*np.ones(len(players)))
    # players['elo_clay_rating'] = pd.Series(np.ones(len(players)))
    # players['elo_hard_rating'] = pd.Series(np.ones(len(players)))
    # players['elo_grass_rating'] = pd.Series(np.ones(len(players)))
    # players['elo_carpet_rating'] = pd.Series(np.ones(len(players)))
    # players['elo_unknown_rating'] = pd.Series(np.ones(len(players)))

    players_simulated_dic = simulate_tour(all_matches, players_dic, k=24, ksi=400, s='delta')

    players_simulated = pd.DataFrame.from_dict(players_simulated_dic, orient='index')

    print(players_simulated.columns)
    print(players.columns)
    exit(1)
    players = players.merge(players_simulated, how='left', on='player_id')\
        .sort_values(by='elo_rating', ascending=False)
    
    players.to_csv('outputs/players_simulated.csv', index=False)


if __name__ == "__main__":
    main()  # Runs the script when executed directly
