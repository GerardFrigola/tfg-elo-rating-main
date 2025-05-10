import pandas as pd
import streamlit as st
import time
import matplotlib.pyplot as plt

def simulate_tour(tour_df:pd.DataFrame, players_df:pd.DataFrame, k, ksi, s, initial_elo, min_games): 
    assert tour_df.isna().sum().sum() == 0, f'nan values in tour_df\n{tour_df.isna().sum()}'

    players_dic = {player_id: {
    'player_id': player_id, 
    'elo_rating': initial_elo, 
    'elo_clay_rating': initial_elo, 
    'elo_hard_rating': initial_elo, 
    'elo_grass_rating': initial_elo, 
    'elo_carpet_rating': initial_elo, 
    'elo_unknown_rating': initial_elo,
    'n_games': 0,
    'last_game': 00000000
    } for player_id in players_df['player_id']}

    elo_history_list = []
    placeholder = st.empty()
    start = time.time()

    total_matches = len(tour_df)
    placeholder.markdown(f"<h6 style='text-align: center; color: black;'>Simulant {total_matches} partits. Això hauria de trigar entre 10 i 20 segons.</h6>", unsafe_allow_html=True)

    year = ''
    for _, m in tour_df.iterrows():
        
        if year != m['match_year']:
            # placeholder.write(f'    Simulating year {m['match_year']}...')
            year = m['match_year']

        # Update elo ratings
        match s:
            case 'delta':
                Sw = 1
                Sl = 0

            case 'thirds': 
                if m['best_of'] != m['num_sets'] or m['best_of'] == 1:
                    Sw = 1
                    Sl = 0
                else: 
                    Sw = 2/3
                    Sl = 1/3

        
        # Algorisme per calcular elo-ratings
        winner_id = m['winner_id']
        loser_id = m['loser_id']
        elo_surface = f'elo_{m['surface'].lower()}_rating'
        match_date = m['tourney_date']
        surface = m['surface']

        old_wr =  players_dic[winner_id]['elo_rating']
        old_lr = players_dic[loser_id]['elo_rating']
        # Surface
        old_slr = players_dic[winner_id][elo_surface]
        old_swr = players_dic[loser_id][elo_surface]

        mu_w = 1 / (1 + pow(10, -(old_wr - old_lr)/ksi))
        mu_l = 1 / (1 + pow(10, -(old_lr - old_wr)/ksi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -(old_swr - old_slr)/ksi))
        mu_sl = 1 / (1 + pow(10, -(old_slr - old_swr)/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors. 
        winner_new_elo = old_wr + k*(Sw - mu_w)
        loser_new_elo = old_lr + k*(Sl - mu_l)
        players_dic[winner_id]['elo_rating'] = winner_new_elo
        players_dic[loser_id]['elo_rating'] = loser_new_elo
        # Surface
        players_dic[winner_id][elo_surface] = old_swr + k*(Sw - mu_sw)
        players_dic[loser_id][elo_surface] = old_slr + k*(Sl - mu_sl)

        players_dic[loser_id]['n_games'] += 1
        players_dic[loser_id]['last_game'] = match_date
        players_dic[winner_id]['n_games'] += 1
        players_dic[winner_id]['last_game'] = match_date

        # Històric
        winner_history = {
            'player_id': winner_id,
            'date': match_date,
            'surface': surface,
            'elo_rating': winner_new_elo
        }
        loser_history = {
            'player_id': loser_id,
            'date': match_date,
            'surface': surface,
            'elo_rating': loser_new_elo
        }

        elo_history_list.append(winner_history)
        elo_history_list.append(loser_history)


    players_simulated: pd.DataFrame = pd.DataFrame.from_dict(players_dic, orient='index')

    ranking: pd.DataFrame = players_df.merge(players_simulated, how='left', on='player_id')\
        .sort_values(by='elo_rating', ascending=False)\
        .reset_index(drop=True)\
        .drop(columns=['elo_unknown_rating'])\
        .round(0)\
        .rename(columns={
            'elo_rating': 'Elo Rating', 
            'elo_clay_rating': 'Clay Elo Rating', 
            'elo_hard_rating': 'Hard Elo Rating', 
            'elo_grass_rating': 'Grass Elo Rating', 
            'elo_carpet_rating': 'Carpet Elo Rating'
        })

    ranking.index += 1

    ranking_filtered = ranking[ranking['n_games']>min_games]

    # TODO: Filtrar jugadors retirats.

    elo_history_df = pd.DataFrame(elo_history_list)\
                        .astype({'date': 'datetime64[ns]'})

    placeholder.empty()
    return ranking_filtered, elo_history_df


def plot_elos_histogram(ranking, col2):
    fig1, ax1 = plt.subplots(figsize=(10, 4.5))
    elos = ranking['Elo Rating'].tolist()
    ax1.hist(elos, bins=50)
    ax1.set_title('Elo Rating Distribution')
    ax1.set_xlabel('Elo Rating')
    ax1.set_ylabel('Frequency')
    col2.pyplot(fig1)


def plot_elo_history_date(ranking, elo_history):
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.set_title('Top 5 Players Elo History')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Elo Rating')

    top_five = ranking.nlargest(5, 'Elo Rating')['player_id'].tolist()
    top_five_elos = elo_history[elo_history['player_id'].isin(top_five)]#.sort_values(by=['date'])

    for player_id in top_five:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id]
        name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
        surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]

        ax2.plot(player_elos['date'], player_elos['elo_rating'], label=f'{name} {surname}')

    ax2.legend()

    st.pyplot(fig2)

def plot_elo_history_ngames(ranking, elo_history):
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.set_title('Top 5 Players Elo History')
    ax3.set_xlabel('Number of Games')
    ax3.set_ylabel('Elo Rating')

    top_five = ranking.nlargest(5, 'Elo Rating')['player_id'].tolist()
    top_five_elos = elo_history[elo_history['player_id'].isin(top_five)].sort_values(by=['date'])

    for player_id in top_five:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id]
        name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
        surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]
        n_games = ranking[ranking['player_id'] == player_id]['n_games'].values[0]
        
        ax3.plot(list(range(n_games)), player_elos['elo_rating'], label=f'{name} {surname}')

    ax3.legend()

    st.pyplot(fig3)

def plot_elo_history_surface(ranking, elo_history, player_id):
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
    surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]
    ax4.set_title(f'Històric de {name} {surname} per superfície')
    ax4.set_xlabel('Superfície')
    ax4.set_ylabel('Elo Rating')

    player_elo_history = elo_history[elo_history['player_id'] == player_id].sort_values(by=['date'])

    for surface in ['Clay', 'Hard', 'Grass', 'Carpet']:
        surface_history = player_elo_history[player_elo_history['surface'] == surface]

        ax4.plot(surface_history['date'], surface_history['elo_rating'], label=f'{surface}')

    ax4.legend()

    st.pyplot(fig4)


def show_plots():
    pass