import os
import sys
import pandas as pd
import numpy as np
from entities import Match, Player
from data import load_all_tours, load_tour_from_csv
from utils import simulate_tour, save_ranking
import argparse  # For command-line arguments (optional)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=int, default=24, required=False)
    parser.add_argument('-xi', type=int, default=400, required=False)
    parser.add_argument('-s', default='delta', required=False)
    parser.add_argument('-tour', default='atp', choices=['atp', 'wta', 'all'], required=False)
    args = parser.parse_args()

    k = args.k
    xi = args.xi
    s = args.s
    tour = args.tour

    match tour: 
        case 'atp' | 'wta': 
            all_tours = load_all_tours(f'data/{tour}_matches', k , xi, s)
            all_tours = simulate_tour(all_tours)
            save_ranking(all_tours, tour)

        case 'all':
            all_atp_tours = load_all_tours('data/atp_matches')
            all_wta_tours = load_all_tours('data/wta_matches')
            all_atp_tours = simulate_tour(all_atp_tours, k , xi, s)
            all_wta_tours = simulate_tour(all_wta_tours, k , xi, s)
            save_ranking(all_atp_tours, tour)
            save_ranking(all_wta_tours, tour)

if __name__ == "__main__":
    main()  # Runs the script when executed directly
