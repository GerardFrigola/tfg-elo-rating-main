import pandas as pd
import streamlit as st
from utils import simulate_tour

st.set_page_config(
    page_title='Elo Rating in Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load data ------------------------
matches_df = pd.read_csv('web/web_data/clean_atp_matches.csv')
players_df = pd.read_csv('web/web_data/clean_atp_players.csv')
assert matches_df.isna().sum().sum() == 0, f'nan values in matches\n{matches_df.isna().sum()}'
assert players_df.isna().sum().sum() == 0, f'nan values in players\n{players_df.isna().sum()}'

# Functions -------------------------
    
def values_changed():
    st.write('Values have changed. Rerun the simulation to see the new results.')

# Sidebar ---------------------------
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Input K-factor', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer', on_change=values_changed)
    ksi = st.number_input('Input xi', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer', on_change=values_changed)
    s = st.selectbox('Input score type:', options=['delta', 'thirds'], index=0, on_change=values_changed)
    show_surfaces = st.checkbox('Show surface ratings', value=False)
    initial_elo = st.number_input('Initial Elo rating', min_value=0, max_value=5000, step=1, value=1500, placeholder='Enter a integer', on_change=values_changed)

    years = list(range(1970, 2025))
    # year_list = st.multiselect('Select the year you want to see:', options=years)

    run_simulation = st.button('Run simulation', key='run_simulation')




# Main page -------------------------
    
st.title('Elo Rating in Tennis')
st.subheader('Ranking')

if run_simulation:
    ranking = simulate_tour(matches_df, players_df, k, ksi, s, initial_elo)

    if show_surfaces:
        st.write(ranking)
    else:
        st.write(ranking[['First Name', 'Last Name', 'Elo Rating', 'Hand', 'Country', 'Height', 'player_id']])

st.divider() # ----------------------------------


# if not year_list:
#     st.write(matches)
# else:
#     st.write(matches[matches['match_year'].isin(year_list)])

