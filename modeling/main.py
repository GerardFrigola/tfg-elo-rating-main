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

    all_atp_tours: Tour = load_tour_from_csv('web/web_data/all_data.csv')
    
    simulate_tour(all_atp_tours)

    ranking_df = save_ranking_to_df(all_atp_tours)

    ranking_df.to_csv('outputs/ranking.csv', index=False)


if __name__ == "__main__":
    main()  # Runs the script when executed directly
