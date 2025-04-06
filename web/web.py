import streamlit as st
import pandas as pd

data = pd.read_csv('../data/atp_matches/atp_matches_1990.csv')

st.write("hello world")

st.write(data)