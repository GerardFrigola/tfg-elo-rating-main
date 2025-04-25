import pandas as pd
import streamlit as st
from entities import Player, Match, Tour
from utils import simulate_tour, save_ranking

st.set_page_config(layout='wide')


data = pd.read_csv('web_data/all_data.csv')

st.title('Elo Rating in Tennis')

k = st.number_input('Input K-factor: (must be an integer)', min_value=1, max_value=200, step=1, value=24, placeholder='Enter a integer')

years = list(range(1970, 2025))

year_list = st.multiselect('Select the year you want to see:', options=years)

if not year_list:
    st.write(data)
else:
    st.write(data[data['match_year'].isin(year_list)])

st.write('Elo ratings:')
all_atp_tours = load_all_tours('data/atp_matches')
all_atp_tours = simulate_tour(all_atp_tours, k , xi, s)
st.progress(0)
