import pandas as pd
import streamlit as st
from entities import Player, Match, Tour
from utils import load_tour_from_csv, simulate_tour, save_ranking_to_df
from time import time, sleep
import os

st.set_page_config(layout='wide')

st.title('Elo Rating in Tennis')

st.write('Hola hola hola 19:27')

st.write(f'Dir: {os.getcwd()}')

data = pd.read_csv('web_data/all_data.csv')

k = st.number_input('Input K-factor: (must be an integer)', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer')

years = list(range(1970, 2025))

year_list = st.multiselect('Select the year you want to see:', options=years)

if not year_list:
    st.write(data)
else:
    st.write(data[data['match_year'].isin(year_list)])

# --- Tour loading ---
all_atp_tours = None
if 'all_atp_tours' not in st.session_state:
    st.session_state.all_atp_tours = None  # Initialize it as None

if st.button('Load all matches'):
    st.session_state.all_atp_tours = load_tour_from_csv('web_data/all_data.csv')
    
all_atp_tours = st.session_state.all_atp_tours
if all_atp_tours:
    st.write(f"Loaded {len(all_atp_tours.matches)} matches.")
#------------------
    
if st.button('Run simulation'):  

    simulate_tour(all_atp_tours)

    ranking_df = save_ranking_to_df(all_atp_tours)

    st.write(ranking_df)


