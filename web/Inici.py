import streamlit as st

st.set_page_config(
    page_title='Welcome!',
    page_icon='🏆',
    layout='wide',
)

st.sidebar.markdown('Selecciona un tour de la barra lateral')

st.markdown("<h1 style='text-align: center; color: black;'>Inici</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>Benvingut a l'aplicació de simulació d'Elo Rating al Tennis</h2>", unsafe_allow_html=True)

st.markdown("<p style='text-align: justify; color: black;'>\
                El tipus de puntuació que fan servir l'ATP i la WTA només té en compte com de bé ho fa cada jugador o jugadora en funció del seu rendiment l'any anterior. Si una persona ho fa millor en un torneig del que ho va fer l'any passat, guanyarà punts. Si ho fa pitjor, en perdrà.\
            </p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: justify; color: black;'>\
                En canvi l\'Elo Rating és un sistema de puntuació que té en compte el rendiment envers la persona contra la que juga, repartint un nombre de punts entre ambdues un cop acaba el partit. El nombre de punts que es reparteixen és més gran com més gran sigui la diferència de puntuacions entre elles.'\
            </p>", unsafe_allow_html=True)
