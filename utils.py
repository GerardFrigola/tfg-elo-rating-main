import pandas as pd
import streamlit as st
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

def simulate_tour(tour_df:pd.DataFrame, players_df:pd.DataFrame, k, ksi, s, initial_elo, min_games, year_to_simulate): 
    assert tour_df.isna().sum().sum() == 0, f'nan values in tour_df\n{tour_df.isna().sum()}'

    total_matches = len(tour_df)
    placeholder = st.empty()
    placeholder.markdown(f"<h6 style='text-align: center; color: black;'>Simulant {total_matches} partits. Trigarà entre 10 i 20 segons.</h6>", unsafe_allow_html=True)

    tour_df = tour_df.sort_values(by='tourney_date', ascending=True)

    if year_to_simulate != 'Tots': 
        tour_df = tour_df[tour_df['tour_year']==year_to_simulate]

    all_players_dic = {player_id: {
            'player_id': player_id, 
            'elo_rating': initial_elo, 
            'elo_clay_rating': initial_elo, 
            'elo_hard_rating': initial_elo, 
            'elo_grass_rating': initial_elo, 
            'elo_carpet_rating': initial_elo, 
            'elo_unknown_rating': initial_elo,
            'n_games': 0,
            'last_game': None,
            'n_wins': 0,
            'n_losses': 0
        } for player_id in players_df['player_id']}

    elo_history_list = []

    year = ''
    for _, m in tour_df.iterrows():
        
        if year != m['tour_year']:
            # placeholder.write(f'    Simulating year {m['match_year']}...')
            year = m['tour_year']

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

        old_wr =  all_players_dic[winner_id]['elo_rating']
        old_lr = all_players_dic[loser_id]['elo_rating']
        # Surface
        old_slr = all_players_dic[winner_id][elo_surface]
        old_swr = all_players_dic[loser_id][elo_surface]

        mu_w = 1 / (1 + pow(10, -(old_wr - old_lr)/ksi))
        mu_l = 1 / (1 + pow(10, -(old_lr - old_wr)/ksi))
        # Surface
        mu_sw = 1 / (1 + pow(10, -(old_swr - old_slr)/ksi))
        mu_sl = 1 / (1 + pow(10, -(old_slr - old_swr)/ksi))

        # Actualitzar els valors dels elo-ratings dels jugadors. 
        winner_new_elo = old_wr + k*(Sw - mu_w)
        loser_new_elo = old_lr + k*(Sl - mu_l)
        all_players_dic[winner_id]['elo_rating'] = winner_new_elo
        all_players_dic[loser_id]['elo_rating'] = loser_new_elo
        # Surface
        all_players_dic[winner_id][elo_surface] = old_swr + k*(Sw - mu_sw)
        all_players_dic[loser_id][elo_surface] = old_slr + k*(Sl - mu_sl)

        all_players_dic[loser_id]['n_games'] += 1
        all_players_dic[loser_id]['last_game'] = match_date
        all_players_dic[winner_id]['n_games'] += 1
        all_players_dic[winner_id]['last_game'] = match_date
        all_players_dic[winner_id]['n_wins'] += 1
        all_players_dic[loser_id]['n_losses'] += 1
        assert all_players_dic[winner_id]['n_games'] == all_players_dic[winner_id]['n_wins'] + all_players_dic[winner_id]['n_losses'],\
            f"Error: n_games != n_wins + n_losses -> {all_players_dic[winner_id]['n_games']} != {all_players_dic[winner_id]['n_wins']} + {all_players_dic[winner_id]['n_losses']}"

        # Històric
        winner_history = {
            'player_id': winner_id,
            'date': match_date,
            'elo_rating': winner_new_elo
        }
        loser_history = {
            'player_id': loser_id,
            'date': match_date,
            'elo_rating': loser_new_elo
        }

        elo_history_list.append(winner_history)
        elo_history_list.append(loser_history)


    players_simulated: pd.DataFrame = pd.DataFrame.from_dict(all_players_dic, orient='index')

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


    ranking_filtered = ranking[(ranking['n_games']>min_games)]# & (ranking['last_game'] > '2023-01-01')].reset_index(drop=True)

    ranking_filtered['rank'] = ranking_filtered.index + 1

    elo_history_df = pd.DataFrame(elo_history_list)\
                        .astype({'date': 'datetime64[ns]'})
    placeholder.empty()
    return ranking_filtered, elo_history_df


def plot_elos_histogram(ranking, col2):
    elos = ranking['Elo Rating'].tolist()
    data = pd.DataFrame({'Elo Rating': elos})
    mean_value = data['Elo Rating'].mean()  # Calculate the mean

    histogram = alt.Chart(data).mark_bar().encode(
        alt.X('Elo Rating:Q', bin=alt.Bin(maxbins=40), title='Elo Rating'),
        alt.Y('count()', title='Frequència')
    ).properties(
        title=alt.TitleParams(text="Distribució de puntuacions", anchor='middle', fontSize=20, fontWeight='bold'),
        width=600,
        height=450
    )

    mean_line = alt.Chart(pd.DataFrame({'mean': [mean_value]})).mark_rule(color='red').encode(
        x='mean:Q'
    )
    
    # Combine histogram and mean line
    chart = (histogram + mean_line).interactive()

    col2.altair_chart(chart)


def plot_elo_history_date(ranking, elo_history):
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.set_title('Top 5 Players Elo History')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Elo Rating')

    top_five = ranking.nlargest(5, 'Elo Rating')['player_id'].tolist()
    top_five_elos = elo_history[elo_history['player_id'].isin(top_five)].sort_values(by=['date'])

    for player_id in top_five:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id]
        name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
        surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]

        ax2.plot(player_elos['date'], player_elos['elo_rating'], label=f'{name} {surname}')

    ax2.xaxis.set_major_locator(mdates.YearLocator(2))  # Major ticks every 2 years
    ax2.xaxis.set_minor_locator(mdates.YearLocator(1))  # Minor ticks every 1 year
    ax2.grid(True, which='major', linestyle='-')  # Add gridlines
    ax2.grid(True, which='minor', linestyle='-')  # Add gridlines
    ax2.legend()    

    st.pyplot(fig2)



def plot_elo_history_date_st(ranking, elo_history, players_ids, start_year, end_year):

    top_five_elos = elo_history[elo_history['player_id'].isin(players_ids)].sort_values(by=['date'])

    # Create a single DataFrame for Altair
    data = []
    for player_id in players_ids:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id].round(0)
        name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
        surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]
        player_elos['Player'] = f'{name} {surname}'  # Create player labels
        data.append(player_elos[['date', 'elo_rating', 'Player']])

    df = pd.concat(data)  # Combine all players into one DataFrame

    # Determine y-axis limits
    min_elo = df['elo_rating'].min() - 100
    max_elo = df['elo_rating'].max() + 100

    # Define Altair line chart
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('date:T', scale=alt.Scale(domain=[start_year, end_year])),
        y=alt.Y('elo_rating:Q', scale=alt.Scale(domain=[min_elo, max_elo])),
        color=alt.Color('Player:N', legend=alt.Legend(orient='top-left'))  # Different colors for different players
    ).properties(
        title=alt.TitleParams(text="Històric Elo Rating per data dels jugadors seleccionats", anchor='middle', fontSize=20, fontWeight='bold'),
        height=600
    ).interactive()

    return chart



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

    ax3.grid(True, which='major', linestyle='-')

    st.pyplot(fig3)

def plot_elo_history_ngames_st(ranking, elo_history, players_ids):

    top_five_elos = elo_history[elo_history['player_id'].isin(players_ids)].sort_values(by=['date'])

    data = []
    for player_id in players_ids:
        player_elos = top_five_elos[top_five_elos['player_id'] == player_id].reset_index(drop=True).round(0)
        name = ranking.loc[ranking['player_id'] == player_id, 'First Name'].values[0]
        surname = ranking.loc[ranking['player_id'] == player_id, 'Last Name'].values[0]
        n_games = len(player_elos)  # Number of recorded Elo ratings
        
        player_elos['Game Number'] = list(range(1, n_games + 1))  # Set x-axis as game count
        player_elos['Player'] = f'{name} {surname}'  # Create player labels
        data.append(player_elos[['Game Number', 'elo_rating', 'Player']])

    df = pd.concat(data)

    # Determine y-axis limits
    min_elo = df['elo_rating'].min() - 100
    max_elo = df['elo_rating'].max() + 100

    # Define Altair line chart
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Game Number:Q', scale=alt.Scale(domain=[1, df['Game Number'].max()])),
        y=alt.Y('elo_rating:Q', scale=alt.Scale(domain=[min_elo, max_elo])),
        color=alt.Color('Player:N', legend=alt.Legend(orient='top-left'))  # Different colors for different players
    ).properties(
        title=alt.TitleParams(text="Històric Elo Rating per partits jugats dels jugadors seleccionats", anchor='middle', fontSize=20, fontWeight='bold'),
        height=600
    ).interactive()
    
    return chart
    

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
