import pandas as pd
import os
from pathlib import Path
from entities import Match, Player, Tour

def clean_tour(df: pd.DataFrame):

    assert df["tourney_id"].isna().sum() == 0, f"tourney_id is NaN. Match: {df['tourney_id'].any()}"
    assert df['tourney_name'].isna().sum() == 0, f"tourney_name is NaN. Match: {df['tourney_id'].any()} "
    # assert df['draw_size'].isna().sum() == 0, f"draw_size is NaN. Match: {df['tourney_id'].any()}"
    assert df['tourney_level'].isna().sum() == 0, f"tourney_level is NaN. Match: {df['tourney_id'].any()}"
    assert df['tourney_date'].isna().sum() == 0, f"tourney_date is NaN. Match: {df['tourney_id'].any()}"
    assert df['match_num'].isna().sum() == 0, f"match_num is NaN. Match: {df['tourney_id'].any()}"
    # assert df['score'].isna().sum() == 0, f"score is NaN. Match: {df['tourney_id'].any()}"
    assert df['best_of'].isna().sum() == 0, f"best_of is NaN. Match: {df['tourney_id'].any()}"
    assert df['round'].isna().sum() == 0, f"round is NaN. Match: {df['tourney_id'].any()}"
    assert df['winner_id'].isna().sum() == 0, f"winner_id is NaN. Match: {df['tourney_id'].any()}"
    assert df['loser_id'].isna().sum() == 0, f"loser_id is NaN"

    df['surface'] = df['surface'].fillna('Unknown')
    assert df['surface'].isna().sum() == 0, f"surface is NaN. Match: {df['tourney_id'].any()}"

    return df

def load_tour_from_csv(file_path: str, tour: Tour = Tour(matches=[], players={}, ranking={})) -> Tour:
    """
    Reads a CSV file and creates a Tour object containing all matches.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Tour: An instance of Tour containing a list of Match objects.
    """
    print(f'    Loading matches from {file_path}')
    df = pd.read_csv(file_path)
    df = clean_tour(df)
    for _, row in df.iterrows():
        # Obtenir id dels dos jugadors del partit
        winner_id = row["winner_id"]
        loser_id = row["loser_id"]

        # Crear els jugadors si encara no existeixen
        if winner_id not in tour.players:
            tour.players[winner_id] = Player(winner_id, row["winner_name"])  # Default ELO rating 0
        if loser_id not in tour.players:
            tour.players[loser_id] = Player(loser_id, row["loser_name"])

        # Guardar la info del partit
        match = Match(
            tourney_id=row["tourney_id"],
            tourney_name=row["tourney_name"],
            draw_size=row["draw_size"],
            surface=row['surface'],
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

def load_all_tours(folder_path: str = '../data') -> Tour: 
    """
    Llegeix tots els fitxers de tours i crea un objecte Tour amb tots els partits de la carpeta 'folder_path'.

    Args: 
        folder_path (str): Ruta a la carpeta que conté els tots fitxers CSV.

    Returns: 
        Tour(): Un objecte Tour que conté tots els partits de la carpeta 'folder_path'.
    """

    mega_tour = Tour()
    
    folder = Path(folder_path)

    for subdir, dirs, files in os.walk(folder):
        for file in sorted(files[:-1]):
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                mega_tour = load_tour_from_csv(file_path, tour=mega_tour)


    return mega_tour
