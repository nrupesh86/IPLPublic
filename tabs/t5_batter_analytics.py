import streamlit as st
from charts.t5ch_batter_avg_sr_by_year import plot_batter_avg_sr_by_year
from charts.t5ch_batter_boundaries_by_year import plot_batter_boundaries_by_year
from charts.t5ch_batter_dismissals_by_year import plot_batter_dismissals_by_year
from charts.t5ch_batter_runs_by_year import plot_batter_runs_by_year
from components.season_filter import season_filter
from services.batter_service import (
    get_career_runs_leader,
    get_player_avg_sr_by_year,
    get_player_boundaries_by_year,
    get_player_dismissals_by_year,
    get_player_runs_by_year,
)


def render(filtered_match_df, df):

    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Batter Analytics",
        key="batter_tab_season_filter",
    )

    tab_df = df[df["year"].isin(tab_selected_years)]

    match_type_option = st.selectbox(
        "Match Type",
        options=["All", "Playoffs & Finals"],
        index=0,
        key="batter_tab_match_type",
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
        key="batter_tab_player_scope",
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
        st.info("No data for the selected filters.")
        return

    batters = sorted(tab_df["batter"].dropna().unique())
    if not batters:
        st.info("No batters in the current selection.")
        return

    career_runs = df.groupby("batter")["runs_batter"].sum()
    leader = get_career_runs_leader(df)

    if leader and leader in batters:
        default_index = batters.index(leader)
    else:
        default_index = batters.index(max(batters, key=lambda b: career_runs.get(b, 0)))

    selected_batter = st.selectbox(
        "Batter",
        options=batters,
        index=default_index,
        key="batter_tab_batter_select",
    )

    pdf = tab_df[tab_df["batter"] == selected_batter].copy()

    if pdf.empty:
        st.info("No balls for this batter in the current selection.")
        return

    st.subheader("Runs by season")

    runs_y = get_player_runs_by_year(pdf)
    fig1 = plot_batter_runs_by_year(runs_y, selected_batter)
    st.plotly_chart(fig1, width="stretch")

    st.divider()
    st.subheader("Batting average & strike rate by season")

    avg_sr = get_player_avg_sr_by_year(tab_df, pdf)
    fig2 = plot_batter_avg_sr_by_year(avg_sr, selected_batter)
    st.plotly_chart(fig2, width="stretch")

    st.divider()
    st.subheader("Boundaries by season")

    bd_y = get_player_boundaries_by_year(pdf)
    fig3 = plot_batter_boundaries_by_year(bd_y, selected_batter)
    st.plotly_chart(fig3, width="stretch")

    st.divider()
    st.subheader("Dismissal types by season")

    dis_y = get_player_dismissals_by_year(tab_df, selected_batter)
    fig4 = plot_batter_dismissals_by_year(dis_y, selected_batter)
    st.plotly_chart(fig4, width="stretch")
