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

# Load Data
if 'atp_matches_df' not in ss:
    ss['atp_matches_df'] = pd.read_csv('web_data/clean_atp_matches.csv')

if 'wta_matches_df' not in ss:
    ss['wta_matches_df'] = pd.read_csv('web_data/clean_wta_matches.csv')



st.markdown("<h1 style='text-align: center; color: black;'>Cercador de partits</h1>", unsafe_allow_html=True)

atp_tab, wta_tab = st.tabs(['ATP', 'WTA'])

with atp_tab:
    st.markdown("<h2 style='text-align: center; color: black;'>ATP</h1>", unsafe_allow_html=True)

    # Streamlit code test
    st.dataframe(ut.filter_atp_dataframe(ss['atp_matches_df']))

with wta_tab:
    st.markdown("<h2 style='text-align: center; color: black;'>WTA</h1>", unsafe_allow_html=True)

    # Streamlit code test
    st.dataframe(ut.filter_wta_dataframe(ss['wta_matches_df']))


st.divider()
st.markdown("<h2 style='text-align: center; color: black;'>Afegir selecció de partit per veure les stats: </h2>", unsafe_allow_html=True)

