import os
import sys
import pandas as pd
import numpy as np
from entities import Match, Player
import argparse  # For command-line arguments (optional)


def main():
    matches2023 = read_match('../data/atp_matches/atp_matches_2023.csv') #type: ignore
    fila = 880
    wrp = matches2023['winner_rank_points'][fila]
    lrp = matches2023['loser_rank_points'][fila]
    wr, lr = compute_ratings(wrp, lrp, K=40, ksi=400) #type: ignore
    print(f'Winner old: {wrp} points.\nWinner new: {wr} points. \n\nLoser old: {lrp}\nLoser new: {lr} points.')

if __name__ == "__main__":
    main()  # Runs the script when executed directly
