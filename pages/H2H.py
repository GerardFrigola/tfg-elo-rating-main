import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from utils import Plots as plot
from utils import Simulation as sim

st.set_page_config(
    page_title='Elo Rating al Tennis',
    page_icon='',
    layout='wide',
    initial_sidebar_state="expanded"
)
# sim.initialize_session_satate()

st.markdown('<h1 style="text-align: center; color: black;">Comparador de jugadors</h1>', unsafe_allow_html=True)

atp_tab, wta_tab = st.tabs(['Masc.', 'Fem.'])


with atp_tab:
    col1, _, col2, _, col3 = st.columns([1, 0.2, 2, 0.2, 1])
    atp_player_dict_options = {
        name: player_id
        for name, player_id in zip(
            ss['atp_nofiltered_ranking']['First Name'] + ' ' + ss['atp_nofiltered_ranking']['Last Name'],
            ss['atp_nofiltered_ranking']['player_id']
        )
    }
    # TODO: Fer que les opcions es guardin al ss    
    atp_h2h_player1 = col1.selectbox(label='', options=atp_player_dict_options.keys(), key='atp_player1', index=0)
    atp_h2h_player2 = col3.selectbox(label='', options=atp_player_dict_options.keys(), key='atp_player2', index=1)

    player1_id = atp_player_dict_options[atp_h2h_player1]
    player2_id = atp_player_dict_options[atp_h2h_player2]

    player1_info = ss['atp_nofiltered_ranking'][ss['atp_nofiltered_ranking']['player_id'] == player1_id]
    player2_info = ss['atp_nofiltered_ranking'][ss['atp_nofiltered_ranking']['player_id'] == player2_id]

    image1 = plot.get_player_image_bytes(player1_info['wikidata_id'].values[0])
    col1.image(image1, use_container_width=True)

    image2 = plot.get_player_image_bytes(player2_info['wikidata_id'].values[0])
    col3.image(image2, use_container_width=True)

    wins_1vs2 = ss['atp_matches_df'][(ss['atp_matches_df']['winner_id']==player1_id) & (ss['atp_matches_df']['loser_id']==player2_id)].value_counts().sum()
    wins_2vs1 = ss['atp_matches_df'][(ss['atp_matches_df']['winner_id']==player2_id) & (ss['atp_matches_df']['loser_id']==player1_id)].value_counts().sum()

    col2.write('')
    col2.write('')
    col2.write('')
    col2.write('')

    # H2H:

    # Victòries enfrontament:
    col2.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 32px; border: 3px solid green; padding: 20px; border-radius: 50px;'>
            <span style='text-align: left; font-weight: bold;'>{wins_1vs2}</span>
            <span style='text-align: center; font-weight: bold;'>VICTÒRIES ENFRONTAMENT</span>
            <span style='text-align: right; font-weight: bold;'>{wins_2vs1}</span>
        </div>
        """, unsafe_allow_html=True
    )
    col2.write('')
    col2.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["elo_rating"].values[0]:.0f}</span>
            <span style='text-align: center;'>ELO RATING</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["elo_rating"].values[0]:.0f}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["n_wins"].values[0]}/{player1_info["n_losses"].values[0]}</span>
            <span style='text-align: center;'>Nº VICTÒRIES/derrotes</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["n_wins"].values[0]}/{player2_info["n_losses"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["n_titles"].values[0]}</span>
            <span style='text-align: left;'>Nº TITOLS</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["n_titles"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; border-bottom: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["max_elo_rating"].values[0]:.0f}</span>
            <span style='text-align: left;'>MAX ELO RATING</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["max_elo_rating"].values[0]:.0f}</span>
        </div>
        """, unsafe_allow_html=True
    )


    # Player 1 info:
    col1.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Rank</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["rank"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Mà</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Hand"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>País</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Country"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Alçada</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Height"].values[0]}cm</span>
        </div>
        """, unsafe_allow_html=True
    )

    # Player 2 info:
    col3.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Rank</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["rank"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Mà</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Hand"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>País</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Country"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Alçada</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Height"].values[0]}cm</span>
        </div>
        """, unsafe_allow_html=True
    )


    st.markdown('<h2 style="text-align: center; color: black;">Enfrontaments</h2>', unsafe_allow_html=True)

    enfrontaments = ss['atp_matches_df'][
        (ss['atp_matches_df']['winner_id']==player1_id) & (ss['atp_matches_df']['loser_id']==player2_id) |
        (ss['atp_matches_df']['winner_id']==player2_id) & (ss['atp_matches_df']['loser_id']==player1_id)
        ]

    st.dataframe(enfrontaments[
            ['match_id',
            'winner_name',
            'loser_name', 
            'score', 
            'tourney_date', 
            'tour_year', 
            'tourney_name',
            'tourney_level',
            'best_of',
            'round',
            'num_sets']
        ].set_index('match_id'))


with wta_tab: 
    col1, _, col2, _, col3 = st.columns([1, 0.2, 2, 0.2, 1])
    wta_player_dict_options = {
        name: player_id
        for name, player_id in zip(
            ss['wta_nofiltered_ranking']['First Name'] + ' ' + ss['wta_nofiltered_ranking']['Last Name'],
            ss['wta_nofiltered_ranking']['player_id']
        )
    }
    # TODO: Fer que les opcions es guardin al ss    
    wta_h2h_player1 = col1.selectbox(label='', options=wta_player_dict_options.keys(), key='wta_player1', index=0)
    wta_h2h_player2 = col3.selectbox(label='', options=wta_player_dict_options.keys(), key='wta_player2', index=1)

    player1_id = wta_player_dict_options[wta_h2h_player1]
    player2_id = wta_player_dict_options[wta_h2h_player2]

    player1_info = ss['wta_nofiltered_ranking'][ss['wta_nofiltered_ranking']['player_id'] == player1_id]
    player2_info = ss['wta_nofiltered_ranking'][ss['wta_nofiltered_ranking']['player_id'] == player2_id]

    image1 = plot.get_player_image_bytes(player1_info['wikidata_id'].values[0])
    col1.image(image1, use_container_width=True)

    image2 = plot.get_player_image_bytes(player2_info['wikidata_id'].values[0])
    col3.image(image2, use_container_width=True)

    wins_1vs2 = ss['wta_matches_df'][(ss['wta_matches_df']['winner_id']==player1_id) & (ss['wta_matches_df']['loser_id']==player2_id)].value_counts().sum()
    wins_2vs1 = ss['wta_matches_df'][(ss['wta_matches_df']['winner_id']==player2_id) & (ss['wta_matches_df']['loser_id']==player1_id)].value_counts().sum()

    col2.write('')
    col2.write('')
    col2.write('')
    col2.write('')

    # H2H:

    # Victòries enfrontament:
    col2.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 32px; border: 3px solid green; padding: 20px; border-radius: 50px;'>
            <span style='text-align: left; font-weight: bold;'>{wins_1vs2}</span>
            <span style='text-align: center; font-weight: bold;'>VICTÒRIES ENFRONTAMENT</span>
            <span style='text-align: right; font-weight: bold;'>{wins_2vs1}</span>
        </div>
        """, unsafe_allow_html=True
    )
    col2.write('')
    col2.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["elo_rating"].values[0]:.0f}</span>
            <span style='text-align: center;'>ELO RATING</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["elo_rating"].values[0]:.0f}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["n_wins"].values[0]}/{player1_info["n_losses"].values[0]}</span>
            <span style='text-align: center;'>Nº VICTÒRIES/derrotes</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["n_wins"].values[0]}/{player2_info["n_losses"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["n_titles"].values[0]}</span>
            <span style='text-align: left;'>Nº TITOLS</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["n_titles"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; border-bottom: 2px solid green; padding: 10px; border-radius: 10px;'>
            <span style='text-align: left; font-weight: bold;'>{player1_info["max_elo_rating"].values[0]:.0f}</span>
            <span style='text-align: left;'>MAX ELO RATING</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["max_elo_rating"].values[0]:.0f}</span>
        </div>
        """, unsafe_allow_html=True
    )


    # Player 1 info:
    col1.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Rank</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["rank"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Mà</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Hand"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>País</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Country"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Alçada</span>
            <span style='text-align: right; font-weight: bold;'>{player1_info["Height"].values[0]}cm</span>
        </div>
        """, unsafe_allow_html=True
    )

    # Player 2 info:
    col3.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-top: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Rank</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["rank"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Mà</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Hand"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>País</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Country"].values[0]}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 24px; border-bottom: 2px solid green; border-left: 2px solid green; border-right: 2px solid green; padding: 10px;'>
            <span style='text-align: left;'>Alçada</span>
            <span style='text-align: right; font-weight: bold;'>{player2_info["Height"].values[0]}cm</span>
        </div>
        """, unsafe_allow_html=True
    )


    st.markdown('<h2 style="text-align: center; color: black;">Enfrontaments</h2>', unsafe_allow_html=True)

    enfrontaments = ss['wta_matches_df'][
        (ss['wta_matches_df']['winner_id']==player1_id) & (ss['wta_matches_df']['loser_id']==player2_id) |
        (ss['wta_matches_df']['winner_id']==player2_id) & (ss['wta_matches_df']['loser_id']==player1_id)
        ]

    st.dataframe(enfrontaments[
            ['match_id',
            'winner_name',
            'loser_name', 
            'score', 
            'tourney_date', 
            'tour_year', 
            'tourney_name',
            'tourney_level',
            'best_of',
            'round',
            'num_sets']
        ].set_index('match_id'))