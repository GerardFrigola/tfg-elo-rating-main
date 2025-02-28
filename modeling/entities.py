# TODO: 
    #   - Crear classe Tourney? --> De moment no interessa tenir una classe tourney ja que els elos s'actualitzen dps de cada match (no com a l'atp que es després de cada tourney)
    #   - Crear classe Tour?
    #   - Necessito els atp_rankings al llarg del temps? O almenys necessito que estiguin a Matc o Player?

class Tour():
    """
    Classe que conté una llista de tots els partits d'un tour, en principi un any sencer
    Un objecte Tour en principi equivaldrà a un fitxer atp_matches_year.csv
    """
    def __init__(self, matches:list[Match]) -> None:
        self.matches = matches 

    def simulate_tour(self) -> None: 
        pass

class Match():
    """
    Classe amb la informació d'un partit de singles.
    """
    def __init__(self, tourney_id, tourney_name, draw_size, tourney_level, tourney_date, match_num, score, best_of, round, winner:Player, loser:Player,):
        self.tourney_id = tourney_id 
        self.tourney_name = tourney_name
        self.draw_size = draw_size
        self.tourney_level = tourney_level
        self.tourney_date = tourney_date
        self.match_id = tourney_id + match_num # a match-specific identifier. Often starting from 1, sometimes counting down from 300, and sometimes arbitrary. 
        self.score = score
        self.best_of = best_of # 3 or 5 games
        self.round = round
        self.winner = winner
        self.loser = loser

    def update_elo_ratings(self) -> None: # a l'atp els ranquings d'actualitzen després de cada torneig, NO després de cada partit
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
        old_wr = self.winner.elo_rating
        old_lr = self.loser.elo_rating

        d_w = old_wr - old_lr
        d_l = old_lr - old_wr

        mu_w = 1 / (1 + pow(10, -d_w/ksi))
        mu_l = 1 / (1 + pow(10, -d_l/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors.
        self.winner.elo_rating = old_wr + K*(Sw - mu_w)
        self.loser.elo_rating = old_lr + K*(Sl - mu_l)

        # TODO: Actualitzar el rank del jugador i el ranking general

class Player():
    def __init__(self, id, name, elo_rating, elo_rank):
        self.id = id
        self.name = name
        self.elo_rating = elo_rating
        self.elo_rank = elo_rank

    

