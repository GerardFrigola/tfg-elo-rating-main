import pandas as pd
import streamlit as st
import streamlit_extras as stx
from streamlit import session_state as ss

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
col11, col12 = col1.columns([1, 1])

col11.markdown(f"""
    <p style='text-align: left; font-size: 24px;'>Elo Rating</p>
    <p style='text-align: left; font-weight: bold; font-size: 32px;'>{(player1_info["Elo Rating"].values[0])}</p>
    """, unsafe_allow_html=True
)

col12.markdown(f"""
    <p style='text-align: right; font-size: 24px;'>Nombre de partits</p>
    <p style='text-align: right; font-weight: bold; font-size: 32px;'>{player1_info["n_games"].values[0]}</p>
    """, unsafe_allow_html=True
)

col11.markdown(f"""
    <p style='text-align: left; font-size: 20px;'>Nombre de victòries</p>
    <p style='text-align: left; font-weight: bold; font-size: 32px;'>{player1_info["n_wins"].values[0]}</p>
    """, unsafe_allow_html=True
)
col12.markdown(f"""
    <p style='text-align: right; font-size: 20px;'>Nombre de derrotes</p>
    <p style='text-align: right; font-weight: bold; font-size: 32px;'>{player1_info["n_losses"].values[0]}</p>
    """, unsafe_allow_html=True
)


# PLAYER 2
player2_info = ss['atp_ranking'][ss['atp_ranking']['player_id'] == player2_id]
col21, col22 = col2.columns([1, 1])
col21.markdown(f"""
    <p style='text-align: left; font-size: 24px;'>Elo Rating</p>
    <p style='text-align: left; font-weight: bold; font-size: 32px;'>{(player2_info["Elo Rating"].values[0])}</p>
    """, unsafe_allow_html=True
)

col22.markdown(f"""
    <p style='text-align: right; font-size: 24px;'>Nombre de partits</p>
    <p style='text-align: right; font-weight: bold; font-size: 32px;'>{player2_info["n_games"].values[0]}</p>
    """, unsafe_allow_html=True
)

col21.markdown(f"""
    <p style='text-align: left; font-size: 20px;'>Nombre de victòries</p>
    <p style='text-align: left; font-weight: bold; font-size: 32px;'>{player2_info["n_wins"].values[0]}</p>
    """, unsafe_allow_html=True
)
col22.markdown(f"""
    <p style='text-align: right; font-size: 20px;'>Nombre de derrotes</p>
    <p style='text-align: right; font-weight: bold; font-size: 32px;'>{player2_info["n_losses"].values[0]}</p>
    """, unsafe_allow_html=True
)
