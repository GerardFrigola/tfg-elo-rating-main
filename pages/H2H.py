import pandas as pd
import streamlit as st
import streamlit_extras as stx
from streamlit import session_state as ss
from io import BytesIO
import requests
from utils import Plots as plot

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='',
    layout='wide',
    initial_sidebar_state="expanded"
)
css='''
[data-testid="metric-container"] {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] label {
    width: fit-content;
    margin: auto;
}
'''
st.markdown('<h1 style="text-align: center; color: black;">Comparador de jugadors</h1>', unsafe_allow_html=True)
# st.markdown('<h2 style="text-align: center; color: black;">ATP</h2>', unsafe_allow_html=True)
col1, _, col2 = st.columns([3, 1, 3])

atp_player_dict_options = {
    name: player_id
    for name, player_id in zip(
        ss['atp_ranking']['First Name'] + ' ' + ss['atp_ranking']['Last Name'],
        ss['atp_ranking']['player_id']
    )
}
player1_name = col1.selectbox(label='', options=atp_player_dict_options.keys(), key='player1')
player2_name = col2.selectbox(label='', options=atp_player_dict_options.keys(), key='player2')

player1_id = atp_player_dict_options[player1_name]
player2_id = atp_player_dict_options[player2_name]

# Què vull ensenyar?
# nom, partits jugats, partits guanyats, partits perduts, percentatge de victòries, Elo rating
player1_info = ss['atp_ranking'][ss['atp_ranking']['player_id'] == player1_id]

image1 = plot.get_player_image_bytes(player1_info['wikidata_id'].values[0])
if image1 is None:
    image1 = 'default_no_profile_pic.png'

col1.image(image1, width=250)


col1.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Elo Rating</span>
        <span style='text-align: right; font-weight: bold;'>{player1_info["Elo Rating"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True)

col1.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de partits</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player1_info["n_games"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)
col1.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de victòries</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player1_info["n_wins"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)
col1.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de derrotes</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player1_info["n_losses"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)


# PLAYER 2
player2_info = ss['atp_ranking'][ss['atp_ranking']['player_id'] == player2_id]

image2 = plot.get_player_image_bytes(player2_info['wikidata_id'].values[0])
if image2 is None:
    image2 = 'default_no_profile_pic.png'

col2.image(image2, width=200)


col2.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Elo Rating</span>
        <span style='text-align: right; font-weight: bold;'>{player2_info["Elo Rating"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True)

col2.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de partits</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player2_info["n_games"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)
col2.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de victòries</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player2_info["n_wins"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)
col2.markdown(f"""
    <div style='display: flex; justify-content: space-between; font-size: 24px;'>
        <span style='text-align: left;'>Nombre de derrotes</span>
        <span style='text-align: right; font-weight: bold; font-size: 32px;'>{player2_info["n_losses"].values[0]}</span>
    </div>
    """, unsafe_allow_html=True
)