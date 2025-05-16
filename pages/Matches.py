import pandas as pd
import streamlit as st
from streamlit import session_state as ss
import utils as ut

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)
st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {1}rem;
                }}
                .reportview-container .main .block-container {{
                    padding-top: {1}rem;
                }}
            </style>
            ''',unsafe_allow_html=True)
# Load Data
atp_matches_df = pd.read_csv('web_data/clean_atp_matches.csv')
wta_matches_df = pd.read_csv('web_data/clean_wta_matches.csv')

# Session state
# if 'atp_start_year_filter' not in ss:
#     ss['atp_start_year'] = 1970 

# if 'atp_end_year_filter' not in ss: 
#     ss['atp_end_year'] = 2024


st.markdown("<h1 style='text-align: center; color: black;'>Cercador de partits</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>ATP</h1>", unsafe_allow_html=True)


# FILTERS #
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

# Years
atp_start_year, atp_end_year = col1.select_slider(
    "Rang d'anys",
    options=list(range(1970, 2027)),
    value=(1970, 2026),
)

# Round
unique_rounds = atp_matches_df['round'].unique()
ronda_filter = col2.multiselect('Ronda', options=unique_rounds,
        help=f'R128=64-ens -- R64=32-ens -- R32=Setzens -- R16=Vuitens de final -- QF: Quarts de final -- SF: Semifinal -- F: Final -- BR: Bye Round -- RR: Round Robin -- ER: Exhibition Round')

# Players
atp_player_dict_options = {
    name: player_id
    for name, player_id in zip(
        ss['atp_ranking']['First Name'] + ' ' + ss['atp_ranking']['Last Name'],
        ss['atp_ranking']['player_id']
    )
}
player_ids = []
players_filter = col3.multiselect('Jugadors', options=atp_player_dict_options.keys())
for player_name in players_filter:
    player_ids.append(atp_player_dict_options[player_name])


# Tournament
unique_tournaments = atp_matches_df['tourney_name'].unique()
tournament_filter = col4.multiselect('Torneig', options=unique_tournaments)

# Surface
unique_surfaces = list(atp_matches_df['surface'].unique())
unique_surfaces.remove('Unknown')
surface_filter = col5.multiselect('Superficie', options=unique_surfaces)

filetered_atp_atp_matches = ut.filter_matches(atp_matches_df, atp_start_year, atp_end_year, ronda_filter, player_ids, tournament_filter, surface_filter)
st.dataframe(filetered_atp_atp_matches.set_index('match_id'), use_container_width=True, hide_index=False)
