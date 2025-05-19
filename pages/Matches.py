import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from utils import Filter as fil
from utils import Simulation as sim

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='🏆',
    layout='wide',
    initial_sidebar_state="expanded"
)
sim.initialize_session_satate()


st.markdown("<h1 style='text-align: center; color: black;'>Cercador de partits</h1>", unsafe_allow_html=True)

atp_tab, wta_tab = st.tabs(['ATP', 'WTA'])

with atp_tab:
    st.markdown("<h2 style='text-align: center; color: black;'>ATP</h1>", unsafe_allow_html=True)

    st.dataframe(fil.filter_atp_dataframe(ss['atp_matches_df']))

with wta_tab:
    st.markdown("<h2 style='text-align: center; color: black;'>WTA</h1>", unsafe_allow_html=True)

    st.dataframe(fil.filter_wta_dataframe(ss['wta_matches_df']))


st.divider()
st.markdown("<h2 style='text-align: center; color: black;'>Afegir selecció de partit per veure les stats: </h2>", unsafe_allow_html=True)

