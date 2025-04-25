import datetime


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.elo_rating = 0
        self.elo_rank: int = None
        self.elo_history = {}  # Dict to store ranking history: {tourney_date: ranking aftermatch}

        #Surface elo ratings and ranks
        self.elo_surf_rating = {'Hard': 0.0, 'Clay': 0.0, 'Carpet': 0.0, 'Grass': 0.0, 'Unknown': 0.0}
        self.elo_surf_rank = {'Hard': 0, 'Clay': 0, 'Carpet': 0, 'Grass': 0, 'Unknown': 0}
        self.elo_surf_history = {'Hard': {}, 'Clay': {}, 'Carpet': {}, 'Grass': {}, 'Unknown':{}}  # Dict to store ranking history


class Match():
    """
    Classe amb la informació d'un partit de singles.
    """
    def __init__(self, tourney_id, tourney_name, draw_size, surface, tourney_level, tourney_date, match_num, score, best_of, round, winner_id, loser_id,):
        self.tourney_id = tourney_id 
        self.tourney_name = tourney_name
        self.draw_size = draw_size
        self.surface = surface
        self.tourney_level = tourney_level # G, F, D, M, A, C, S
        self.tourney_date = tourney_date
        self.match_id = str(tourney_id) + str(match_num) # a match-specific identifier. Often starting from 1, sometimes counting down from 300, and sometimes arbitrary. 
        self.score = score
        self.best_of = best_of # 3 or 5 games
        self.round = round
        self.winner_id = winner_id
        self.loser_id = loser_id


class Tour():
    """
    Classe que conté una llista de tots els partits d'un tour, en principi un any sencer
    Un objecte Tour en principi equivaldrà a un fitxer atp_matches_year.csv
    """
    def __init__(self, 
                 matches:list[Match]=[], 
                 players:dict[int, Player]={}, 
                 ranking: dict[Player, int]={}, # TODO: Que la clau sigui l'id i no la classe sencera. 
                 surf_ranking: dict[str, dict[Player, int]]={'Hard': {}, 'Clay': {}, 'Carpet': {}, 'Grass':{}, 'Unknown':{}}
                ) -> None:
        self.matches = matches 
        self.players = players
        self.ranking = ranking
        self.surf_ranking = surf_ranking

    def update_elo_ratings(self, winner:Player, loser:Player, tourney_date, surface) -> None: # a l'atp els ranquings d'actualitzen després de cada torneig, NO després de cada partit
        """
        Mètode per actualitzar els elo ratings dels jugadors d'un partit.
        """
        assert surface in ['Grass', 'Clay', 'Carpet', 'Hard', 'Unknown'], f'Surface {surface} not suported. {tourney_date}'
        
        # TODO: Decidir d'on treiem els paràmetres, de moment fixats
        # TODO: Canviar l'score (Sw, Sl) perquè depengui del resultat del partit
        ksi = 400
        K = 50
        Sw = 1 
        Sl = 0

        # Algorisme per calcular elo-ratings
        old_wr = winner.elo_rating
        old_lr = loser.elo_rating
        # Surface
        old_slr = winner.elo_surf_rating[surface]
        old_swr = loser.elo_surf_rating[surface]

        d_w = old_wr - old_lr
        d_l = old_lr - old_wr
        # Surface
        d_sw = old_swr - old_slr
        d_sl = old_slr - old_swr

        mu_w = 1 / (1 + pow(10, -d_w/ksi))
        mu_l = 1 / (1 + pow(10, -d_l/ksi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -d_sw/ksi))
        mu_sl = 1 / (1 + pow(10, -d_sl/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors.
        winner.elo_rating = round(old_wr + K*(Sw - mu_w), 3)
        loser.elo_rating = round(old_lr + K*(Sl - mu_l), 3)
        # Surface
        winner.elo_surf_rating[surface] = round(old_swr + K*(Sw - mu_sw), 3)
        loser.elo_surf_rating[surface] = round(old_slr + K*(Sl - mu_sl), 3)
        
        winner.elo_history[tourney_date] = winner.elo_rating
        loser.elo_history[tourney_date] = loser.elo_rating
        # Surface
        winner.elo_surf_history[surface][tourney_date] = winner.elo_surf_rating[surface]
        loser.elo_surf_history[surface][tourney_date] = loser.elo_surf_rating[surface]
        

    def update_elo_ranking(self, winner:Player, loser:Player, surface):
        # Update Elo rating in the dictionaries
        self.ranking[winner] = winner.elo_rating
        self.ranking[loser] = loser.elo_rating
        self.surf_ranking[surface][winner] = winner.elo_surf_rating[surface]
        self.surf_ranking[surface][loser] = loser.elo_surf_rating[surface]

        # Get the sorted list of players (keeping original order in a list to avoid re-sorting everyone)
        sorted_players = sorted(self.ranking.keys(), key=lambda p: self.ranking[p], reverse=True)
        sorted_players_surf = sorted(self.surf_ranking[surface].keys(), key=lambda p: self.surf_ranking[surface][p], reverse=True)

        # Update ranks only if necessary
        for new_rank, player in enumerate(sorted_players, start=1):
            if player.elo_rank != new_rank:
                player.elo_rank = new_rank  # Update player's rank

        for new_rank, player in enumerate(sorted_players_surf, start=1): 
            if player.elo_surf_rank[surface] != new_rank:
                player.elo_surf_rank[surface] = new_rank


    def simulate_tour(self) -> None: 
        print(f'Simulating tour...\n {len(self.matches)} matches.\n')
        year = ''
        for match in self.matches:
            if year != match.match_id[:4]:
                print(f'    Simulating year {match.match_id[:4]}...')
                year = match.match_id[:4]

            winner = self.players[match.winner_id]
            loser = self.players[match.loser_id]
            surface = match.surface
            date = match.tourney_date
            # TODO: Calcular aqui el score S

            self.update_elo_ratings(winner, loser, date, surface)
            self.update_elo_ranking(winner, loser, surface)

    def save_ranking(self) :
        """
        Guarda el ranking sencer un cop acabat el tour
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        filename = f'rankings_{timestamp}'

        with open(f'./outputs/{filename}.txt', 'w') as f:
            # Column headers with proper alignment
            f.write(f'{'Rank'}  {'Name':>4} {"Rating":>30} {'H. Rank':>10} {"H. Rating":>4} {'Cl. Rank':>10} {"Cl. Rating":>4} {'Ca. Rank':>10} {"Ca. Rating":>4} {'G. Rank':>10} {"G. Rating":>4}\n')  
            
            for rank, (player, rating) in enumerate(sorted(self.ranking.items(), key=lambda item: item[1], reverse=True), start=1): 
                hard_rating = player.elo_surf_rating['Hard']
                hard_rank = player.elo_surf_rank['Hard']
                clay_rating = player.elo_surf_rating['Clay']
                clay_rank = player.elo_surf_rank['Clay']
                carpet_rating = player.elo_surf_rating['Carpet']
                carpet_rank = player.elo_surf_rank['Carpet']
                grass_rating = player.elo_surf_rating['Grass']
                grass_rank = player.elo_surf_rank['Grass']
                

                f.write(f'{rank}. {player.name:>4} {rating:>30} {hard_rank:>10}. {hard_rating:>4} {clay_rank:>10}. {clay_rating:>4} {carpet_rank:>10}. {carpet_rating:>4} {grass_rank:>10}. {grass_rating:>4} \n')

            print(f'\nRanking saved to outputs/{filename}.txt')
        
