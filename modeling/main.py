import os
import sys
import pandas as pd
import numpy as np

# Import your modules
import argparse  # For command-line arguments (optional)


def score(wl):
    # TODO: Implementar una fórmula per l'score en funció de la puntuació
    if wl=='winner': return 1
    elif wl=='loser': return 0
    else: raise ValueError('Only "winner" or "loser" is accepted as wl')

def compute_ratings(ri_old, rj_old, K, ksi):
    pass

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
