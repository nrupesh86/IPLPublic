import streamlit as st
from charts.t2ch_top_venues import plot_top_venues
from charts.t2ch_matches_per_city import plot_matches_per_city
from charts.t2ch_venue_team_result import plot_venue_team_results
from charts.t2ch_innings_result_by_venue import plot_innings_results_by_venue
from charts.t2ch_toss_impact_by_venue import plot_toss_impact_by_venue
from components.season_filter import season_filter
from services.venue_service import get_team_results_by_venue, get_innings_results_by_venue, get_toss_impact_by_venue

def render(filtered_match_df):

    # -------- Reusable Season Filter --------
    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Venue Analysis",
        key="venue_tab_season_filter"
    )

    tab_match_df = filtered_match_df[
        filtered_match_df["year"].isin(tab_selected_years)
    ]

    # ---------- Top Venues ----------
    st.subheader("Top Venues")

    # ---- Calculate max venues dynamically ----
    total_venues = tab_match_df["venue"].nunique()

    # Generate increments of 5
    options = list(range(5, total_venues + 1, 5))

    # Ensure max value is included if not multiple of 5
    if total_venues not in options:
        options.append(total_venues)

    # Sort just in case
    options = sorted(options)

    # Default = min(15, max available)
    default_index = options.index(min(15, total_venues)) if min(15, total_venues) in options else 0

    top_n = st.selectbox(
        "Select Top N Venues",
        options=options,
        index=default_index
    )

    fig1 = plot_top_venues(tab_match_df, top_n)
    st.plotly_chart(fig1, width="stretch")

    st.divider()

    # ---------- Matches by City ----------
    st.subheader("Matches by City")

    # ---- Calculate max venues dynamically ----
    total_cities = filtered_match_df["city"].nunique()

    # Generate increments of 5
    options_cities = list(range(5, total_cities + 1, 5))

    # Ensure max value is included if not multiple of 5
    if total_cities not in options_cities:
        options_cities.append(total_cities)

    # Sort just in case
    options_cities = sorted(options_cities)

    # Default = min(15, max available)
    default_index_cities = options_cities.index(min(15, total_cities)) if min(15, total_cities) in options_cities else 0

    top_n_cities = st.selectbox(
        "Select Top N Cities",
        options=options_cities,
        index=default_index_cities
    )

    fig2 = plot_matches_per_city(tab_match_df, top_n_cities)
    st.plotly_chart(fig2, width="stretch")

    st.divider()

    st.subheader("Team Results by Venue")
    summary = get_team_results_by_venue(tab_match_df, top_n)
    fig3 = plot_venue_team_results(summary)
    st.plotly_chart(fig3, width="stretch")

    st.divider()

    st.subheader("Batting First vs Bowling First Wins by Venue")
    innings_df = get_innings_results_by_venue(tab_match_df, top_n)
    fig4 = plot_innings_results_by_venue(innings_df)
    st.plotly_chart(fig4, width="stretch")

    st.divider()

    st.subheader("Toss Impact by Venue")
    toss_df = get_toss_impact_by_venue(tab_match_df, top_n)
    fig5 = plot_toss_impact_by_venue(toss_df)
    st.plotly_chart(fig5, width="stretch")