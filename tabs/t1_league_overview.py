import streamlit as st
from components.season_filter import season_filter
from services.player_service import get_players_per_season
from services.boundary_service import get_boundaries_per_season
from services.toss_service import get_toss_impact_per_season, get_toss_impact_overall, get_toss_decision_per_season
from services.match_result_service import get_innings_win_per_season, get_innings_win_overall
from charts.t1ch_matches_per_season import plot_matches_per_season
from charts.t1ch_players_per_season import plot_players_per_season
from charts.t1ch_boundaries_per_season import plot_boundaries_per_season
from charts.t1ch_toss_impact_per_season import plot_toss_impact_per_season
from charts.t1ch_toss_impact_overall import plot_toss_impact_overall
from charts.t1ch_toss_decision_per_season import plot_toss_decision_per_season
from charts.t1ch_innings_win_per_season import plot_innings_win_per_season
from charts.t1ch_innings_win_overall import plot_innings_win_overall

def render(filtered_match_df, df):

    # -------- Reusable Season Filter --------
    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for League Overview",
        key="league_tab_season_filter"
    )

    tab_match_df = filtered_match_df[
        filtered_match_df["year"].isin(tab_selected_years)
    ]

    tab_df = df[
        df["year"].isin(tab_selected_years)
    ]

    ######### Matches per Season #########
    st.subheader("Matches per Season")

    fig1 = plot_matches_per_season(tab_match_df)
    st.plotly_chart(fig1, width='stretch')

    ######### Players per Season #########
    st.subheader("Players per Season")

    players_per_season = get_players_per_season(tab_df)
    fig2 = plot_players_per_season(players_per_season)
    st.plotly_chart(fig2, width='stretch')
    
    ######### Boundaries per Season #########
    st.subheader("Boundaries per Season")

    boundaries_df = get_boundaries_per_season(df, filtered_match_df)
    fig3 = plot_boundaries_per_season(boundaries_df)
    st.plotly_chart(fig3, width='stretch')

    ######### Toss Impact #########
    st.subheader("Toss Win vs Match Outcome (%)")

    toss_df = get_toss_impact_per_season(filtered_match_df)
    fig4 = plot_toss_impact_per_season(toss_df)
    st.plotly_chart(fig4, width='stretch')

    ######### Overall Toss Impact #########
    st.subheader("Overall Toss Win vs Match Outcome (%)")

    toss_impact_overall = get_toss_impact_overall(filtered_match_df)
    fig5 = plot_toss_impact_overall(toss_impact_overall)

    st.plotly_chart(fig5, width='stretch')

    ######### Toss Decision Pattern #########
    st.subheader("Toss Decision Pattern (%)")

    toss_decision_df = get_toss_decision_per_season(filtered_match_df)
    fig6 = plot_toss_decision_per_season(toss_decision_df)

    st.plotly_chart(fig6, width='stretch')

    ######### Innings Win Pattern #########
    st.subheader("Bat First vs Bowl First Win %")

    innings_df = get_innings_win_per_season(filtered_match_df)
    fig7 = plot_innings_win_per_season(innings_df)

    st.plotly_chart(fig7, width='stretch')

    ######### Overall Innings Win Pattern #########
    st.subheader("Overall Bat First vs Bowl First Win %")

    innings_win_overall = get_innings_win_overall(filtered_match_df)
    fig8 = plot_innings_win_overall(innings_win_overall)

    st.plotly_chart(fig8, width='stretch')