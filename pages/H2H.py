import pandas as pd
import streamlit as st
from streamlit import session_state as ss

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='',
    layout='wide',
    initial_sidebar_state="expanded"
)

st.markdown('<h1 style="text-align: center; color: black;">Comparador de jugadors</h1>', unsafe_allow_html=True)
# st.markdown('<h2 style="text-align: center; color: black;">ATP</h2>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

player1 = col1.selectbox(label='', options=ss['atp_ranking']['First Name'] + ' ' + ss['atp_ranking']['Last Name'], key='player1')
player2 = col3.selectbox(label='', options=ss['atp_ranking']['First Name'] + ' ' + ss['atp_ranking']['Last Name'], key='player2')

col1.write()