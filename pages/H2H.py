import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='',
    layout='wide',
    initial_sidebar_state="expanded"
)

col1, col2, col3 = st.columns([1, 2, 1])

st.markdown('<h1 style="text-align: center; color: black;">Comparador de jugadors</h1>', unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; color: black;">Se vienen cositas...</h2>', unsafe_allow_html=True)