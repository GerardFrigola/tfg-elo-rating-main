import pandas as pd
import os
from entities import Match, Player


def load_match(path):
    match_df = pd.read_csv(path)
    # TODO: guardar la info en un objecte match
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

def load_tour(atp_matches: os.Path) -> None:
    """
    Carregar la info de tots els matches d'un fitxer tipus 'atp_matches_2019.csv' i els fica en un dataframe de matches. 
    """
    file = pd.read_csv(atp_matches)
    
    pass