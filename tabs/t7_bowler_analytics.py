import streamlit as st
from components.season_filter import season_filter
from services.bowler_service import (
    get_career_wickets_leader,
    get_bowler_wickets_by_year,
    get_bowler_wickets_per_100_by_year,
    get_bowler_economy_by_year,
    get_bowler_dot_balls_by_year,
    get_bowler_dot_balls_per_100_by_year,
    get_bowler_boundaries_by_year,
    get_bowler_boundaries_per_100_by_year,
)
from charts.t7ch_bowler_wickets_by_year import plot_bowler_wickets_by_year
from charts.t7ch_bowler_wickets_per_100_by_year import plot_bowler_wickets_per_100_by_year
from charts.t7ch_bowler_economy_by_year import plot_bowler_economy_by_year
from charts.t7ch_bowler_dot_balls_by_year import plot_bowler_dot_balls_by_year
from charts.t7ch_bowler_dot_balls_per_100_by_year import plot_bowler_dot_balls_per_100_by_year
from charts.t7ch_bowler_boundaries_by_year import plot_bowler_boundaries_by_year
from charts.t7ch_bowler_boundaries_per_100_by_year import plot_bowler_boundaries_per_100_by_year


def render(filtered_match_df, df):
    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Bowler Analytics",
        key="bowler_analytics_tab_season_filter",
    )

    tab_df = df[df["year"].isin(tab_selected_years)]

    match_type_option = st.selectbox(
        "Match Type",
        options=["All", "Playoffs & Finals"],
        index=0,
        key="bowler_analytics_tab_match_type",
    )

    if match_type_option == "Playoffs & Finals":
        playoff_final_stages = [
            "Final",
            "Semi Final",
            "3rd Place Play-Off",
            "Qualifier 1",
            "Qualifier 2",
            "Eliminator",
            "Elimination Final",
        ]
        tab_df = tab_df[tab_df["stage"].isin(playoff_final_stages)]

    player_scope = st.selectbox(
        "Player Scope",
        options=["All Players", "Active Players"],
        index=0,
        key="bowler_analytics_tab_player_scope",
    )

    if player_scope == "Active Players":
        available_years = sorted(tab_df["year"].dropna().unique().tolist())
        if available_years:
            latest_two_years = available_years[-2:]
            active_bowlers = (
                tab_df[tab_df["year"].isin(latest_two_years)]["bowler"]
                .dropna()
                .unique()
                .tolist()
            )
            tab_df = tab_df[tab_df["bowler"].isin(active_bowlers)]

    if tab_df.empty:
        st.info("No data for the selected filters.")
        return

    bowlers = sorted(tab_df["bowler"].dropna().unique())
    if not bowlers:
        st.info("No bowlers in the current selection.")
        return

    career_leader = get_career_wickets_leader(tab_df)
    if career_leader and career_leader in bowlers:
        default_index = bowlers.index(career_leader)
    else:
        bowler_wk = tab_df.dropna(subset=["bowler", "player_out", "wicket_kind"]).groupby("bowler").size()
        default_bowler = bowler_wk.idxmax() if not bowler_wk.empty else bowlers[0]
        default_index = bowlers.index(default_bowler) if default_bowler in bowlers else 0

    selected_bowler = st.selectbox(
        "Bowler",
        options=bowlers,
        index=default_index,
        key="bowler_analytics_tab_bowler_select",
    )

    pdf = tab_df[tab_df["bowler"] == selected_bowler].copy()
    if pdf.empty:
        st.info("No data for selected bowler in current filter set.")
        return

    st.subheader("Wickets by season")
    wk_by_year = get_bowler_wickets_by_year(pdf)
    st.plotly_chart(plot_bowler_wickets_by_year(wk_by_year, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Wickets per 100 balls by season")
    wk_per_100 = get_bowler_wickets_per_100_by_year(pdf)
    st.plotly_chart(plot_bowler_wickets_per_100_by_year(wk_per_100, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Economy by season")
    econ_by_year = get_bowler_economy_by_year(pdf)
    st.plotly_chart(plot_bowler_economy_by_year(econ_by_year, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Dot balls by season")
    dot_by_year = get_bowler_dot_balls_by_year(pdf)
    st.plotly_chart(plot_bowler_dot_balls_by_year(dot_by_year, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Dot balls per 100 balls by season")
    dot_per_100 = get_bowler_dot_balls_per_100_by_year(pdf)
    st.plotly_chart(plot_bowler_dot_balls_per_100_by_year(dot_per_100, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Boundaries conceded by season")
    boundaries_by_year = get_bowler_boundaries_by_year(pdf)
    st.plotly_chart(plot_bowler_boundaries_by_year(boundaries_by_year, selected_bowler), width="stretch")

    st.divider()
    st.subheader("Boundaries conceded per 100 balls by season")
    boundaries_per_100 = get_bowler_boundaries_per_100_by_year(pdf)
    st.plotly_chart(plot_bowler_boundaries_per_100_by_year(boundaries_per_100, selected_bowler), width="stretch")
