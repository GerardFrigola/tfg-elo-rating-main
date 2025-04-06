import datetime
import matplotlib.pyplot as plt


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.elo_rating = 0
        self.elo_rank: int = None
        self.elo_history = {}  # Dict to store ranking history: {tourney_date: ranking aftermatch}
        self.n_games = 0  # Number of games played
        self.n_wins = 0
        self.n_losses = 0

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
                 surf_ranking: dict[str, dict[Player, int]]={'Hard': {}, 'Clay': {}, 'Carpet': {}, 'Grass':{}, 'Unknown':{}},
                 k:any=24, xi:int=400, s:str='delta'
                ) -> None:
        self.matches = matches 
        self.players = players
        self.ranking = ranking
        self.surf_ranking = surf_ranking
        self.k = k 
        self.xi = xi
        self.s = s

    def update_elo_ratings(self, winner:Player, loser:Player, tourney_date, surface) -> None: # a l'atp els ranquings d'actualitzen després de cada torneig, NO després de cada partit
        """
        Mètode per actualitzar els elo ratings dels jugadors d'un partit.
        """
        
        xi = self.xi
        k = self.k
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

        mu_w = 1 / (1 + pow(10, -d_w/xi))
        mu_l = 1 / (1 + pow(10, -d_l/xi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -d_sw/xi))
        mu_sl = 1 / (1 + pow(10, -d_sl/xi))

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

        winner.n_games += 1
        loser.n_games += 1
        winner.n_wins += 1
        loser.n_losses += 1
        
        surfaces = ['Hard', 'Clay', 'Carpet', 'Grass', 'Unknown']
        surfaces.remove(surface)
        
        # Other surfaces stay the same rating for both players
        for s in surfaces: 
            if winner.elo_surf_history[s]:
                last_winner_date = max(winner.elo_surf_history[s]) 
                last_winner_rating = winner.elo_surf_history[s][last_winner_date] 
            else: # if history is empty, keep to 1200
                last_winner_rating = 1200
            winner.elo_surf_history[s][tourney_date] = last_winner_rating

            if loser.elo_surf_history[s]:
                last_loser_date = max(loser.elo_surf_history[s]) 
                last_loser_rating = loser.elo_surf_history[s][last_loser_date] 
            else: # if history is empty, keep to 1200
                last_loser_rating = 1200
            loser.elo_surf_history[s][tourney_date] = last_loser_rating
   

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


      
