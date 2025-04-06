import datetime
from entities import Tour

def simulate_tour(tour: Tour) -> None: 
    print(f'Simulating tour...\n {len(tour.matches)} matches.\n')
    year = ''
    for match in tour.matches:
        if year != match.match_id[:4]:
            print(f'    Simulating year {match.match_id[:4]}...')
            year = match.match_id[:4]

        winner = tour.players[match.winner_id]
        loser = tour.players[match.loser_id]
        surface = match.surface
        date = match.tourney_date
        # TODO: Calcular aqui el score S

        tour.update_elo_ratings(winner, loser, date, surface)
        tour.update_elo_ranking(winner, loser, surface) 

    return tour 

def save_ranking(tour: Tour, tour_type: str) :
    """
    Guarda el ranking sencer un cop acabat el tour
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f'{tour_type}_rankings_{timestamp}'
    path = f'./outputs/{tour_type}/{filename}.txt'

    with open(path, 'w') as f:
        # Column headers with proper alignment
        # Encabezado con anchos fijos
        f.write(f'{"Rank":<6} {"Name":<20} {"Rating":>10} {"H. Rank":>10} {"H. Rating":>10} {"Cl. Rank":>10} {"Cl. Rating":>10} {"Ca. Rank":>10} {"Ca. Rating":>10} {"G. Rank":>10} {"G. Rating":>10}\n')

        # Filas de datos
        for rank, (player, rating) in enumerate(sorted(tour.ranking.items(), key=lambda item: item[1], reverse=True), start=1): 
            hard_rating = player.elo_surf_rating['Hard']
            hard_rank = player.elo_surf_rank['Hard']
            clay_rating = player.elo_surf_rating['Clay']
            clay_rank = player.elo_surf_rank['Clay']
            carpet_rating = player.elo_surf_rating['Carpet']
            carpet_rank = player.elo_surf_rank['Carpet']
            grass_rating = player.elo_surf_rating['Grass']
            grass_rank = player.elo_surf_rank['Grass']

            # Escribe cada fila con anchos fijos
            f.write(f'{rank:<6} {player.name:<20} {rating:>10.2f} {hard_rank:>10} {hard_rating:>10.2f} {clay_rank:>10} {clay_rating:>10.2f} {carpet_rank:>10} {carpet_rating:>10.2f} {grass_rank:>10} {grass_rating:>10.2f}\n')
