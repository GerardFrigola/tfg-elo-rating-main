import pandas as pd
import streamlit as st
from streamlit import session_state as ss

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Load Data
atp_matches_df = pd.read_csv('web_data/clean_atp_matches.csv')
wta_matches_df = pd.read_csv('web_data/clean_wta_matches.csv')

# Session state
if 'filters_start_year' not in ss:
    ss['atp_start_year'] = 1970 

if 'atp_end_year' not in ss: 
    ss['atp_end_year'] = 2024


st.markdown("<h1 style='text-align: center; color: black;'>Cercador de partits</h1>", unsafe_allow_html=True)

# Filters
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
st.header('Se vienen cositas...')
sex = col1.selectbox('Torneig', options=['ATP', 'WTA'], key='tournament')

atp_start_year, atp_end_year = col2.select_slider(
    "Selecciona el rang dels anys que vols veure",
    options=list(range(1970, 2027)),
    value=(1970, 2026),
)

ronda = col3.selectbox('Ronda', options= ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F',  'BR',  'RR', 'ER'], key='round',
        help=f'R128=64-ens -- R64=32-ens -- R32=Setzens -- R16=Vuitens de final -- QF: Quarts de final -- SF: Semifinal -- F: Final -- BR: Bye Round -- RR: Round Robin -- ER: Exhibition Round')

match sex:
    case 'ATP':
        st.dataframe(atp_matches_df[
            ['tourney_date',
            'tourney_name',
            'surface',
            'round',
            'winner_name',
            'score',
            'loser_name',
            'match_id']
        ])
    case 'WTA':
        st.dataframe(wta_matches_df)

