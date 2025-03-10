class Player():
    def __init__(self, id, name, elo_rating, elo_rank):
        self.id = id
        self.name = name
        self.elo_rating = elo_rating
        self.elo_rank = elo_rank


class Match():
    """
    Classe amb la informació d'un partit de singles.
    """
    def __init__(self, tourney_id, tourney_name, draw_size, tourney_level, tourney_date, match_num, score, best_of, round, winner_id, loser_id,):
        self.tourney_id = tourney_id 
        self.tourney_name = tourney_name
        self.draw_size = draw_size
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
    def __init__(self, matches:list[Match], players:dict[int, Player], ranking: dict[Player, int]) -> None:
        self.matches = matches 
        self.players = players
        self.ranking = ranking

    def update_elo_ratings(self, winner:Player, loser:Player) -> None: # a l'atp els ranquings d'actualitzen després de cada torneig, NO després de cada partit
        """
        Mètode per actualitzar els elo ratings dels jugadors d'un partit.
        """
        
        # TODO: Decidir d'on treiem els paràmetres, de moment fixats
        # TODO: Canviar l'score (Sw, Sl) perquè depengui del resultat del partit
        ksi = 400
        K = 40
        Sw = 1 
        Sl = 0

        # Algorisme per calcular elo-ratings
        old_wr = winner.elo_rating
        old_lr = loser.elo_rating

        d_w = old_wr - old_lr
        d_l = old_lr - old_wr

        mu_w = 1 / (1 + pow(10, -d_w/ksi))
        mu_l = 1 / (1 + pow(10, -d_l/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors.
        winner.elo_rating = round(old_wr + K*(Sw - mu_w), 3)
        loser.elo_rating = round(old_lr + K*(Sl - mu_l), 3)


    def update_elo_ranking(self, winner:Player, loser:Player):
        # Update Elo rating in the dictionary
        self.ranking[winner] = winner.elo_rating
        self.ranking[loser] = loser.elo_rating

        # Get the sorted list of players (keeping original order in a list to avoid re-sorting everyone)
        sorted_players = sorted(self.ranking.keys(), key=lambda p: self.ranking[p], reverse=True)

        # Update ranks only if necessary
        for new_rank, player in enumerate(sorted_players, start=1):
            if player.elo_rank != new_rank:
                player.elo_rank = new_rank  # Update player's rank


    def simulate_tour(self) -> None: 
        print(f'Simulating tour...\n {len(self.matches)} matches.')
        for match in self.matches:
            print(f'Simulating match {match.match_id[4:]}...')
            winner = self.players[match.winner_id]
            loser = self.players[match.loser_id]

            # TODO: Calcular aqui el score S

            self.update_elo_ratings(winner, loser)
            self.update_elo_ranking(winner, loser)

    def save_ranking(self) :
        """
        Guarda el ranking sencer un cop acabat el tour
        """
        with open('ranking.txt', 'w') as f:
            f.write(f'{'Rank  Name':<25} {"Rating":>10}\n')  # Column headers with proper alignment
            
            for rank, (player, rating) in enumerate(sorted(self.ranking.items(), key=lambda item: item[1], reverse=True), start=1): 
                f.write(f'{rank}.  {player.name:<25} {rating:>10}')
            