import streamlit as st
from charts.t6ch_top_wicket_takers import plot_top_wicket_takers
from charts.t6ch_top_wickets_per_100_balls import plot_top_wickets_per_100_balls
from charts.t6ch_top_dot_balls_per_100_balls import plot_top_dot_balls_per_100_balls
from charts.t6ch_least_boundaries_per_100_balls import plot_least_boundaries_per_100_balls
from charts.t6ch_top_economy_bowlers import plot_top_economy_bowlers
from charts.t6ch_top_dot_ball_bowlers import plot_top_dot_ball_bowlers
from charts.t6ch_least_boundary_giving_bowlers import plot_least_boundary_giving_bowlers
from components.season_filter import season_filter
from services.bowling_service import get_top_wicket_takers, get_top_wickets_per_100_balls, get_top_dot_balls_per_100_balls, get_least_boundaries_per_100_balls, get_top_economy_bowlers, get_top_dot_ball_bowlers, get_least_boundary_giving_bowlers


def render(filtered_match_df, df):

    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Bowling Analytics",
        key="bowling_tab_season_filter",
    )

    tab_df = df[df["year"].isin(tab_selected_years)]

    match_type_option = st.selectbox(
        "Match Type",
        options=["All", "Playoffs & Finals"],
        index=0,
        key="bowling_tab_match_type",
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
        key="bowling_tab_player_scope",
    )

    if player_scope == "Active Players":
        available_years = sorted(tab_df["year"].dropna().unique().tolist())
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

    total_bowlers = tab_df["bowler"].dropna().nunique()
    if total_bowlers == 0:
        st.info("No bowling data for the selected season(s).")
        return

    # Calculate maximum overs bowled
    bowler_overs = tab_df.groupby("bowler")["valid_ball"].sum() // 6
    max_overs = bowler_overs.max() if not bowler_overs.empty else 0
    min_overs_options = list(range(10, int(max_overs) + 1, 10))
    if not min_overs_options:
        min_overs_options = [0]

    st.subheader("Top Wicket Taking Bowlers")

    wickets_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in wickets_options:
        wickets_options.append(total_bowlers)
    wickets_options = sorted(set(wickets_options))

    wickets_default_index = (
        wickets_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in wickets_options
        else 0
    )

    top_n_wickets = st.selectbox(
        "Select Top N Bowlers",
        options=wickets_options,
        index=wickets_default_index,
        key="wickets_top_n",
    )

    min_overs_wickets = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="wickets_min_overs",
    )

    sort_by_wickets = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="wickets_sort_by",
    )

    wickets_df = get_top_wicket_takers(tab_df, top_n_wickets, sort_by_wickets, min_overs_wickets)
    fig1 = plot_top_wicket_takers(wickets_df, top_n_wickets)
    st.plotly_chart(fig1, width="stretch")

    st.divider()
    st.subheader("Top Wicket Takers per 100 Balls")

    wickets_per_100_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in wickets_per_100_options:
        wickets_per_100_options.append(total_bowlers)
    wickets_per_100_options = sorted(set(wickets_per_100_options))

    wickets_per_100_default_index = (
        wickets_per_100_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in wickets_per_100_options
        else 0
    )

    top_n_wickets_per_100 = st.selectbox(
        "Select Top N Bowlers",
        options=wickets_per_100_options,
        index=wickets_per_100_default_index,
        key="wickets_per_100_top_n",
    )

    min_overs_wickets_per_100 = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="wickets_per_100_min_overs",
    )

    sort_by_wickets_per_100 = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="wickets_per_100_sort_by",
    )

    wickets_per_100_df = get_top_wickets_per_100_balls(tab_df, top_n_wickets_per_100, sort_by_wickets_per_100, min_overs_wickets_per_100)
    fig1b = plot_top_wickets_per_100_balls(wickets_per_100_df, top_n_wickets_per_100)
    st.plotly_chart(fig1b, width="stretch")

    st.divider()
    st.subheader("Top Economy Bowlers")

    economy_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in economy_options:
        economy_options.append(total_bowlers)
    economy_options = sorted(set(economy_options))

    economy_default_index = (
        economy_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in economy_options
        else 0
    )

    top_n_economy = st.selectbox(
        "Select Top N Bowlers",
        options=economy_options,
        index=economy_default_index,
        key="economy_top_n",
    )

    min_overs_economy = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="economy_min_overs",
    )

    sort_by_economy = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="economy_sort_by",
    )

    economy_df = get_top_economy_bowlers(tab_df, top_n_economy, sort_by_economy, min_overs_economy)
    fig2 = plot_top_economy_bowlers(economy_df, top_n_economy)
    st.plotly_chart(fig2, width="stretch")

    st.divider()
    st.subheader("Top Dot Ball Bowlers")

    dot_ball_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in dot_ball_options:
        dot_ball_options.append(total_bowlers)
    dot_ball_options = sorted(set(dot_ball_options))

    dot_ball_default_index = (
        dot_ball_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in dot_ball_options
        else 0
    )

    top_n_dot_balls = st.selectbox(
        "Select Top N Bowlers",
        options=dot_ball_options,
        index=dot_ball_default_index,
        key="dot_balls_top_n",
    )

    min_overs_dot_balls = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="dot_balls_min_overs",
    )

    sort_by_dot_balls = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="dot_balls_sort_by",
    )

    dot_balls_df = get_top_dot_ball_bowlers(tab_df, top_n_dot_balls, sort_by_dot_balls, min_overs_dot_balls)
    fig3 = plot_top_dot_ball_bowlers(dot_balls_df, top_n_dot_balls)
    st.plotly_chart(fig3, width="stretch")

    st.divider()
    st.subheader("Top Dot Ball Bowlers per 100 Balls")

    dot_balls_per_100_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in dot_balls_per_100_options:
        dot_balls_per_100_options.append(total_bowlers)
    dot_balls_per_100_options = sorted(set(dot_balls_per_100_options))

    dot_balls_per_100_default_index = (
        dot_balls_per_100_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in dot_balls_per_100_options
        else 0
    )

    top_n_dot_balls_per_100 = st.selectbox(
        "Select Top N Bowlers",
        options=dot_balls_per_100_options,
        index=dot_balls_per_100_default_index,
        key="dot_balls_per_100_top_n",
    )

    min_overs_dot_balls_per_100 = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="dot_balls_per_100_min_overs",
    )

    sort_by_dot_balls_per_100 = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="dot_balls_per_100_sort_by",
    )

    dot_balls_per_100_df = get_top_dot_balls_per_100_balls(tab_df, top_n_dot_balls_per_100, sort_by_dot_balls_per_100, min_overs_dot_balls_per_100)
    fig3b = plot_top_dot_balls_per_100_balls(dot_balls_per_100_df, top_n_dot_balls_per_100)
    st.plotly_chart(fig3b, width="stretch")

    st.divider()
    st.subheader("Least Boundary Giving Bowlers")

    boundaries_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in boundaries_options:
        boundaries_options.append(total_bowlers)
    boundaries_options = sorted(set(boundaries_options))

    boundaries_default_index = (
        boundaries_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in boundaries_options
        else 0
    )

    top_n_boundaries = st.selectbox(
        "Select Top N Bowlers",
        options=boundaries_options,
        index=boundaries_default_index,
        key="boundaries_top_n",
    )

    min_overs_boundaries = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="boundaries_min_overs",
    )

    sort_by_boundaries = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="boundaries_sort_by",
    )

    boundaries_df = get_least_boundary_giving_bowlers(tab_df, top_n_boundaries, sort_by_boundaries, min_overs_boundaries)
    fig4 = plot_least_boundary_giving_bowlers(boundaries_df, top_n_boundaries)
    st.plotly_chart(fig4, width="stretch")

    st.divider()
    st.subheader("Least Boundary Giving Bowlers per 100 Balls")

    boundaries_per_100_options = list(range(5, total_bowlers + 1, 5))
    if total_bowlers not in boundaries_per_100_options:
        boundaries_per_100_options.append(total_bowlers)
    boundaries_per_100_options = sorted(set(boundaries_per_100_options))

    boundaries_per_100_default_index = (
        boundaries_per_100_options.index(min(15, total_bowlers))
        if min(15, total_bowlers) in boundaries_per_100_options
        else 0
    )

    top_n_boundaries_per_100 = st.selectbox(
        "Select Top N Bowlers",
        options=boundaries_per_100_options,
        index=boundaries_per_100_default_index,
        key="boundaries_per_100_top_n",
    )

    min_overs_boundaries_per_100 = st.selectbox(
        "Minimum Overs Bowled",
        options=min_overs_options,
        index=0,
        key="boundaries_per_100_min_overs",
    )

    sort_by_boundaries_per_100 = st.selectbox(
        "Sort By",
        options=["Total", "PowerPlay", "Mid", "Death"],
        index=0,
        key="boundaries_per_100_sort_by",
    )

    boundaries_per_100_df = get_least_boundaries_per_100_balls(tab_df, top_n_boundaries_per_100, sort_by_boundaries_per_100, min_overs_boundaries_per_100)
    fig5 = plot_least_boundaries_per_100_balls(boundaries_per_100_df, top_n_boundaries_per_100)
    st.plotly_chart(fig5, width="stretch")