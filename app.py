import streamlit as st
from utils.data_loader import load_data
from services.match_service import build_match_df
from components.season_filter import season_filter
from tabs import (
    t1_league_overview,
    t2_venue_analytics,
    t3_team_analytics,
    t4_batting_analytics,
    t5_batter_analytics,
    t6_bowling_analytics,
    t7_bowler_analytics,
)

st.set_page_config(layout="wide")
st.title("🏏 IPL Analytics Dashboard")
st.markdown("Designed and developed by Nrupesh Ganji &copy; NCG Global Enterprises", unsafe_allow_html=True)

############# Load data ##############
df = load_data()

############# Build match df ##############
match_df = build_match_df(df)

############# Global Season Filter ##############
selected_years = season_filter(
    df,
    label="Select Season(s)",
    key="global_season_filter",
    location="sidebar"
)

filtered_match_df = match_df[
    match_df["year"].isin(selected_years)
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "League Overview",
        "Venue Analytics",
        "Team Analytics",
        "Batting Analytics",
        "Batter Analytics",
        "Bowling Analytics",
        "Bowler Analytics",
    ]
)

with tab1:
    t1_league_overview.render(filtered_match_df, df)

with tab2:
    t2_venue_analytics.render(filtered_match_df)

with tab3:
    t3_team_analytics.render(filtered_match_df)

with tab4:
    t4_batting_analytics.render(filtered_match_df, df)

with tab5:
    t5_batter_analytics.render(filtered_match_df, df)

with tab6:
    t6_bowling_analytics.render(filtered_match_df, df)

with tab7:
    t7_bowler_analytics.render(filtered_match_df, df)