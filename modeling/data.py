import pandas as pd
import os
from pathlib import Path
from entities import Match, Player, Tour


def load_tour_from_csv(file_path: str, tour: Tour = Tour(matches=[], players={}, ranking={})) -> Tour:
    """
    Reads a CSV file and creates a Tour object containing all matches.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Tour: An instance of Tour containing a list of Match objects.
    """
    print(f'Loading matches from {file_path}')
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        # Obtenir id dels dos jugadors del partit
        winner_id = row["winner_id"]
        loser_id = row["loser_id"]

        # Crear els jugadors si encara no existeixen
        if winner_id not in tour.players:
            tour.players[winner_id] = Player(winner_id, row["winner_name"], 0, None)  # Default ELO rating 0
        if loser_id not in tour.players:
            tour.players[loser_id] = Player(loser_id, row["loser_name"], 0, None)

        # Guardar la info del partit
        match = Match(
            tourney_id=row["tourney_id"],
            tourney_name=row["tourney_name"],
            draw_size=row["draw_size"],
            tourney_level=row["tourney_level"],
            tourney_date=row["tourney_date"],
            match_num=row["match_num"],
            score=row["score"],
            best_of=row["best_of"],
            round=row["round"],
            winner_id=winner_id,
            loser_id=loser_id,
        )

        tour.matches.append(match)

    return tour

def load_all_tours(folder_path: str = '/Users/FRIGO/Desktop/Escriptori (MacBook Air)/MATCAD/5e/TFG/tfg-elo-rating-main/data') -> Tour: 
    """
    Llegeix tots els fitxers de tours i crea un objecte Tour amb tots els partits de la carpeta 'folder_path'.

    Args: 
        folder_path (str): Ruta a la carpeta que conté els tots fitxers CSV.

    Returns: 
        Tour(): Un objecte Tour que conté tots els partits de la carpeta 'folder_path'.
    """

    mega_tour = Tour(matches=[], players={}, ranking={})
    
    for subdir, dirs, files in os.walk(Path(folder_path)):
        for file in sorted(files[:-1]):
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                print(file_path)
                mega_tour = load_tour_from_csv(file_path, tour=mega_tour)
    


    return mega_tour