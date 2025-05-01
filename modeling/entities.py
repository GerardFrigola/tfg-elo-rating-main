import datetime


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.elo_rating = 0
        self.elo_rank: int = None
        self.elo_history = {}  # Dict to store ranking history: {tourney_date: ranking aftermatch}

        #Surface elo ratings and ranks
        self.elo_surf_rating: dict = {'Hard': 0.0, 'Clay': 0.0, 'Carpet': 0.0, 'Grass': 0.0, 'Unknown': 0.0}
        self.elo_surf_rank: dict = {'Hard': 0, 'Clay': 0, 'Carpet': 0, 'Grass': 0, 'Unknown': 0}
        self.elo_surf_history: dict = {'Hard': {}, 'Clay': {}, 'Carpet': {}, 'Grass': {}, 'Unknown':{}}  # Dict to store ranking history


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

    Attributes:
        matches: list[Match]
        players: dict[player_id:int, Player]
        ranking: dict[player_id:int, elo_rating:float]
        surf_ranking: dict[surface:str, dict[player_id:int, elo_rating:float]]

    """

    def __init__(self, 
                 matches:list[Match]=[], 
                 players:dict[int, Player]={}, 
                 ranking: dict[int, int]={}, # TODO: Que la clau sigui l'id i no la classe sencera. FET!
                 surf_ranking: dict[str, dict[int, int]]={'Hard': {}, 'Clay': {}, 'Carpet': {}, 'Grass':{}, 'Unknown':{}}
                ) -> None:
        self.matches = matches 
        self.players = players
        self.ranking = ranking
        self.surf_ranking = surf_ranking 

    def update_elo_ratings(self, winner:Player, loser:Player, tourney_date, surface, k=24, ksi=400, score='delta') -> None: # a l'atp els ranquings d'actualitzen després de cada torneig, NO després de cada partit
        """
        Mètode per actualitzar els elo ratings dels jugadors d'un partit.
        """
        assert surface in ['Grass', 'Clay', 'Carpet', 'Hard', 'Unknown'], f'Surface {surface} not suported. {tourney_date}'
        
        # TODO: Decidir d'on treiem els paràmetres, de moment fixats
        # TODO: Canviar l'score (Sw, Sl) perquè depengui del resultat del partit
        
        match score:
            case 'delta':
                Sw = 1 
                Sl = 0

            case 'pensar el nom':
                pass

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
        winner.elo_rating = round(old_wr + k*(Sw - mu_w), 3)
        loser.elo_rating = round(old_lr + k*(Sl - mu_l), 3)
        # Surface
        winner.elo_surf_rating[surface] = round(old_swr + k*(Sw - mu_sw), 3)
        loser.elo_surf_rating[surface] = round(old_slr + k*(Sl - mu_sl), 3)
        
        winner.elo_history[tourney_date] = winner.elo_rating
        loser.elo_history[tourney_date] = loser.elo_rating
        # Surface
        winner.elo_surf_history[surface][tourney_date] = winner.elo_surf_rating[surface]
        loser.elo_surf_history[surface][tourney_date] = loser.elo_surf_rating[surface]
        

    def update_elo_ranking(self, winner:Player, loser:Player, surface):
        # Update Elo rating in the dictionaries
        winner_id = winner.id
        loser_id = loser.id
        
        self.ranking[winner_id] = self.players[winner_id].elo_rating
        self.ranking[loser_id] = self.players[loser_id].elo_rating
        self.surf_ranking[surface][winner_id] = self.players[winner_id].elo_surf_rating[surface]
        self.surf_ranking[surface][loser_id] = self.players[loser_id].elo_surf_rating[surface]

        # Get the sorted list of players ids (keeping original order in a list to avoid re-sorting everyone)
        sorted_players_ids = sorted(self.ranking.keys(), key=lambda p_id: self.ranking[p_id], reverse=True)
        sorted_players_surf_ids = sorted(self.surf_ranking[surface].keys(), key=lambda p_id: self.surf_ranking[surface][p_id], reverse=True)

        # Update ranks only if necessary
        for new_rank, player_id in enumerate(sorted_players_ids, start=1):
            if self.players[player_id].elo_rank != new_rank:
                self.players[player_id].elo_rank = new_rank  # Update player's rank

        for new_rank, player_id in enumerate(sorted_players_surf_ids, start=1): 
            if self.players[player_id].elo_surf_rank[surface] != new_rank:
                self.players[player_id].elo_surf_rank[surface] = new_rank

