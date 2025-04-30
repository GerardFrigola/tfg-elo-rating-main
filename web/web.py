import pandas as pd
import streamlit as st
from entities import Player, Match, Tour
from utils import load_tour_from_csv, simulate_tour, save_ranking_to_df
from time import time, sleep
import os

st.set_page_config(
    page_title='Elo Rating in Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)
################################
# Load data
matches = pd.read_csv('web/web_data/all_data.csv')
players = pd.read_csv('web/web_data/atp_players.csv')

################################
# Sidebar
with st.sidebar:
    st.title('Filtres')

    k = st.number_input('Input K-factor: (must be an integer)', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer')
    xi = st.number_input('Input xi: (must be a integer)', min_value=100, max_value=1000, step=1, value=400, placeholder='Enter a integer')
    
    years = list(range(1970, 2025))
    year_list = st.multiselect('Select the year you want to see:', options=years)


if not year_list:
    st.write(matches)
else:
    st.write(matches[matches['match_year'].isin(year_list)])

# --- Tour loading ---
all_atp_tours = None
if 'all_atp_tours' not in st.session_state:
    st.session_state.all_atp_tours = None  # Initialize it as None

if st.button('Load all matches'):
    st.session_state.all_atp_tours = load_tour_from_csv('web/web_data/all_data.csv') # If run in local is 'web_data/all_data.csv' else 'web/web_data/all_data.csv'
    
all_atp_tours = st.session_state.all_atp_tours
if all_atp_tours:
    st.write(f"Loaded {len(all_atp_tours.matches)} matches.")
#------------------
    
if st.button('Run simulation'):  

    simulate_tour(all_atp_tours)

    ranking_df = save_ranking_to_df(all_atp_tours)

    st.write(ranking_df)


