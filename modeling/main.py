import os
import sys
import pandas as pd
import numpy as np

# Import your modules
import argparse  # For command-line arguments (optional)

def read_match(path):
    match_df = pd.read_csv(path)
    return match_df[[
        'tourney_id', 
        'tourney_name', 
        'surface',
        'draw_size',
        'tourney_level',
        'tourney_date',
        'match_num', # a match-specific identifier. Often starting from 1, sometimes counting down from 300, and sometimes arbitrary. 
        'score', 
        'best_of', # 3 or 5 games
        'round', 
        'winner_rank',
        'winner_rank_points',
        'loser_rank',
        'loser_rank_points',
        'winner_id',
        'winner_seed', # Seedings are used to separate the top players in a draw so that they will not meet in the early rounds of a tournament.
        'winner_entry', # it determines whether a player has a sufficiently high ranking to gain direct acceptance into the main draw of a tournament.
        'winner_name',
        'loser_id',
        'loser_seed', 
        'loser_entry',
        'loser_name']]



def score(wl):
    # TODO: Implementar una fórmula per l'score en funció de la puntuació
    if wl=='winner': return 1
    elif wl=='loser': return 0
    else: raise ValueError('Only "winner" or "loser" is accepted as wl')

def compute_ratings(ri_old, rj_old, K, ksi):
    # El jugador 'i' serà sempre el guanyador. 
    d_ij = ri_old - rj_old
    d_ji = rj_old - ri_old

    mu_ij = 1 / (1 + pow(10, -d_ij/ksi))
    mu_ji = 1 / (1 + pow(10, -d_ji/ksi))

    Sij = score('winner')
    Sji = score('loser')

    ri_new = ri_old + K*(Sij - mu_ij)
    rj_new = rj_old + K*(Sji - mu_ji)

    return ri_new, rj_new

def main():
    
    # Example: Parse command-line arguments
    # parser = argparse.ArgumentParser(description="This is my script")
    # parser.add_argument("--name", type=str, help="Your name")
    # args = parser.parse_args()
    
    # # Example usage
    # if args.name:
    #     print(f"Hello, {args.name}!")
    
    matches2023 = read_match('../data/atp_matches/atp_matches_2023.csv')
    fila = 880
    wrp = matches2023['winner_rank_points'][fila]
    lrp = matches2023['loser_rank_points'][fila]
    wr, lr = compute_ratings(wrp, lrp, K=40, ksi=400)
    print(f'Winner old: {wrp} points.\nWinner new: {wr} points. \n\nLoser old: {lrp}\nLoser new: {lr} points.')

if __name__ == "__main__":
    main()  # Runs the script when executed directly
