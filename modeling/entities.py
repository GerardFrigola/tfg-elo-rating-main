class Match():
    """
    De moment té moltissims atributs i he de decidir quins faig servir i quins no. 
    """
    # TODO: 
    #   - Que aquest init no tingui tants atributs de jugadors sino que rebi jugadors directament
    #   - Crear classe Tourney?
    #   - Crear classe Tour?

    def __init__(self, tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date, match_num, score, best_of, round,
                 w_atp_rank, w_atp_rank_points, l_atp_rank, l_atp_rank_points, w_id, w_seed, w_entry, w_name, l_id, l_seed, l_entry, l_name):
        self.tourney_id = tourney_id 
        self.tourney_name = tourney_name
        self.surface = surface
        self.draw_size = draw_size
        self.tourney_level = tourney_level
        self.tourney_date = tourney_date
        self.match_num = match_num # a match-specific identifier. Often starting from 1, sometimes counting down from 300, and sometimes arbitrary. 
        self.score = score
        self.best_of = best_of # 3 or 5 games
        self.round = round
        self.w_atp_rank = w_atp_rank
        self.w_atp_rank_points = w_atp_rank_points
        self.l_atp_rank = l_atp_rank
        self.l_atp_rank_points = l_atp_rank_points
        self.w_id = w_id
        self.w_seed = w_seed # Seedings are used to separate the top players in a draw so that they will not meet in the early rounds of a tournament.
        self.w_entry = w_entry # it determines whether a player has a sufficiently high ranking to gain direct acceptance into the main draw of a tournament.
        self.w_name = w_name
        self.l_id = l_id
        self.l_seed = l_seed
        self.l_entry = l_entry
        self.l_name = l_name

    def update_ratings(match: Match) -> None:
        """
        De qui hauria de ser aquest mètode, de Match o de Player?
        """
        # 0. Decidir d'on treiem els paràmetres, de moment fixats
        # 1. Extraure id dels jugadors del partit
        # 2. Amb l'id, extraure els elos antics dels jugadors
        # 3. Calcular elo ratings
        # 4. Fer update dels ratings i del rank 

        # El jugador 'i' serà sempre el guanyador. 
        d_ij = ri_old - rj_old
        d_ji = rj_old - ri_old

        mu_ij = 1 / (1 + pow(10, -d_ij/ksi))
        mu_ji = 1 / (1 + pow(10, -d_ji/ksi))

        Sij = score('winner')
        Sji = score('loser')

        ri_new = ri_old + K*(Sij - mu_ij)
        rj_new = rj_old + K*(Sji - mu_ji)

        return ri_new, rj_new


class Player():
    def __init__(self, id, name, surname, hand, dob, ioc, height, wikidata_id, elo_rating, elo_rank):
        self.id = id
        self.name = name
        self.surname = surname # Ajuntar amb self.name
        self.hand = hand
        self.dob = dob # ????
        self.ioc = ioc
        self.height = height
        self.wikidata_id = wikidata_id
        self.elo_rating = elo_rating
        self.elo_rank = elo_rank

