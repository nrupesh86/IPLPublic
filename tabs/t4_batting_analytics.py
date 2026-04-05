import streamlit as st
from charts.t4ch_top_batting_average import plot_top_batting_average
from charts.t4ch_dismissal_types import plot_dismissal_types
from charts.t4ch_top_boundaries import plot_top_boundaries
from charts.t4ch_top_run_scorers import plot_top_run_scorers
from components.season_filter import season_filter
from services.batting_service import (
    get_dismissal_type_rankings,
    get_batting_average_rankings,
    get_boundary_rankings,
    get_top_run_scorers,
)


def render(filtered_match_df, df):

    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Batting Analysis",
        key="batting_tab_season_filter",
    )

    tab_df = df[df["year"].isin(tab_selected_years)]

    match_type_option = st.selectbox(
        "Match Type",
        options=["All", "Playoffs & Finals"],
        index=0,
        key="batting_tab_match_type",
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
        key="batting_tab_player_scope",
    )

    if player_scope == "Active Players":
        available_years = sorted(tab_df["year"].dropna().unique().tolist())
        latest_two_years = available_years[-2:]

        active_batters = (
            tab_df[tab_df["year"].isin(latest_two_years)]["batter"]
            .dropna()
            .unique()
            .tolist()
        )
        tab_df = tab_df[tab_df["batter"].isin(active_batters)]

    if tab_df.empty:
        st.info("No batting data for the selected filters.")
        return

    st.subheader("Top Run Scorers")

    total_batters = tab_df["batter"].dropna().nunique()
    if total_batters == 0:
        st.info("No batting data for the selected season(s).")
        return

    options = list(range(5, total_batters + 1, 5))
    if total_batters not in options:
        options.append(total_batters)
    options = sorted(set(options))

    default_index = (
        options.index(min(15, total_batters))
        if min(15, total_batters) in options
        else 0
    )

    top_n = st.selectbox(
        "Select Top N Batters",
        options=options,
        index=default_index,
    )

    scorers_df = get_top_run_scorers(tab_df, top_n)
    fig = plot_top_run_scorers(scorers_df, top_n)
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("Top Batting Averages")

    max_runs_player = int(tab_df.groupby("batter")["runs_batter"].sum().max())
    if max_runs_player < 500:
        st.info(
            "Batting average chart needs at least one player with 500+ runs "
            "in the selected season(s)."
        )
        return

    min_runs_options = list(range(500, max_runs_player + 500, 500))
    min_runs = st.selectbox(
        "Minimum runs (for eligibility)",
        options=min_runs_options,
        index=0,
        key="batting_avg_min_runs",
    )
    sort_by_label = st.selectbox(
        "Sort by",
        options=["Strike rate", "Average"],
        index=0,
        key="batting_avg_sort_by",
    )
    sort_by_key = "strike_rate" if sort_by_label == "Strike rate" else "average"
    avg_rankings = get_batting_average_rankings(
        tab_df, min_runs, sort_by=sort_by_key
    )
    eligible_avg = len(avg_rankings)
    if eligible_avg == 0:
        st.info(
            f"No batters meet the minimum of {min_runs:,} runs with at least one dismissal."
        )
    else:
        options_avg = list(range(5, eligible_avg + 1, 5))
        if eligible_avg not in options_avg:
            options_avg.append(eligible_avg)
        options_avg = sorted(set(options_avg))

        default_index_avg = (
            options_avg.index(min(15, eligible_avg))
            if min(15, eligible_avg) in options_avg
            else 0
        )

        top_n_avg = st.selectbox(
            "Select Top N Batters",
            options=options_avg,
            index=default_index_avg,
            key="batting_avg_top_n",
        )

        avg_df = avg_rankings.head(top_n_avg)
        fig_avg = plot_top_batting_average(
            avg_df, top_n_avg, min_runs, sort_by_label
        )
        st.plotly_chart(fig_avg, width="stretch")

    st.divider()

    st.subheader("Top Boundary Hitters")

    min_runs_bd = st.selectbox(
        "Minimum runs (for eligibility)",
        options=min_runs_options,
        index=0,
        key="batting_bd_min_runs",
    )
    sort_bd_label = st.selectbox(
        "Sort by",
        options=["Sixes", "Fours", "Combined boundaries"],
        index=0,
        key="batting_bd_sort",
    )
    sort_bd_key = {"Sixes": "sixes", "Fours": "fours", "Combined boundaries": "combined"}[
        sort_bd_label
    ]
    boundary_rankings = get_boundary_rankings(
        tab_df, min_runs_bd, sort_by=sort_bd_key
    )
    eligible_bd = len(boundary_rankings)
    if eligible_bd == 0:
        st.info(
            f"No batters meet the minimum of {min_runs_bd:,} runs in the selected season(s)."
        )
        return

    options_bd = list(range(5, eligible_bd + 1, 5))
    if eligible_bd not in options_bd:
        options_bd.append(eligible_bd)
    options_bd = sorted(set(options_bd))

    default_index_bd = (
        options_bd.index(min(15, eligible_bd))
        if min(15, eligible_bd) in options_bd
        else 0
    )

    top_n_bd = st.selectbox(
        "Select Top N Batters",
        options=options_bd,
        index=default_index_bd,
        key="batting_bd_top_n",
    )

    boundary_df = boundary_rankings.head(top_n_bd)
    fig_bd = plot_top_boundaries(
        boundary_df, top_n_bd, min_runs_bd, sort_bd_label
    )
    st.plotly_chart(fig_bd, width="stretch")

    st.divider()

    st.subheader("Dismissal Types (Top Batters)")

    min_runs_dis = st.selectbox(
        "Minimum runs (for eligibility)",
        options=min_runs_options,
        index=0,
        key="batting_dis_min_runs",
    )

    dismissal_long = get_dismissal_type_rankings(
        tab_df, min_runs=min_runs_dis, top_n=top_n_bd
    )
    eligible_dis = dismissal_long["player"].nunique() if not dismissal_long.empty else 0
    if eligible_dis == 0:
        st.info(
            f"No batters meet the minimum of {min_runs_dis:,} runs with at least one dismissal."
        )
        return

    # Reuse the same Top N pattern
    options_dis = list(range(5, eligible_dis + 1, 5))
    if eligible_dis not in options_dis:
        options_dis.append(eligible_dis)
    options_dis = sorted(set(options_dis))

    default_index_dis = (
        options_dis.index(min(15, eligible_dis))
        if min(15, eligible_dis) in options_dis
        else 0
    )

    top_n_dis = st.selectbox(
        "Select Top N Batters",
        options=options_dis,
        index=default_index_dis,
        key="batting_dis_top_n",
    )

    dismissal_long = get_dismissal_type_rankings(
        tab_df, min_runs=min_runs_dis, top_n=top_n_dis
    )
    fig_dis = plot_dismissal_types(dismissal_long, top_n_dis, min_runs_dis)
    st.plotly_chart(fig_dis, width="stretch")
