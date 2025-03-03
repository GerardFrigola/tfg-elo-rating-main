import os
import sys
import pandas as pd
import numpy as np
from entities import Match, Player
from data import load_tour_from_csv
import argparse  # For command-line arguments (optional)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', required=True)
    args = parser.parse_args()
    
    file_path = '../data/atp_matches/atp_matches_' + str(args.y) + '.csv'
    tour = load_tour_from_csv(file_path)
    tour.simulate_tour()
    tour.print_ranking()


if __name__ == "__main__":
    main()  # Runs the script when executed directly
