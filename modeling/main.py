import os
import sys
import pandas as pd
import numpy as np
from entities import Match, Player
from data import load_all_tours, load_tour_from_csv
import argparse  # For command-line arguments (optional)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-k', required=True)
    # parser.add_argument('-xi', required=True)
    # args = parser.parse_args()

    # k = args.k
    # xi = args.xi
    
    print('Loading all matches...')
    all_tours = load_all_tours('data/atp_matches')
    print(f'{len(all_tours.matches)} matches loaded.')
    # file_path = '../data/atp_matches/atp_matches_' + str(args.y) + '.csv'
    # tour = load_tour_from_csv(file_path)
    all_tours.simulate_tour()
    all_tours.save_ranking()


if __name__ == "__main__":
    main()  # Runs the script when executed directly
