import pandas as pd
import os
from entities import Match, Player, Tour


def load_tour_from_csv(file_path: str) -> Tour:
    """
    Reads a CSV file and creates a Tour object containing all matches.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Tour: An instance of Tour containing a list of Match objects.
    """
    
    df = pd.read_csv(file_path)

    matches = []
    players = {}  # Dictionary to store Player objects to avoid duplicates

    for _, row in df.iterrows():
        winner_id = row["winner_id"]
        loser_id = row["loser_id"]

        # Get or create the Player objects
        if winner_id not in players:
            players[winner_id] = Player(winner_id, row["winner_name"], 0, None)  # Default ELO rating 0
        if loser_id not in players:
            players[loser_id] = Player(loser_id, row["loser_name"], 0, None)

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

        matches.append(match)

    return Tour(matches, players, {})
