import streamlit as st
from components.season_filter import season_filter
from services.team_service import get_titles_finals_by_team, get_playoff_appearances_wins_by_team, get_head_to_head_win, get_team_win_pct, get_team_win_pct_by_season
from charts.t3ch_titles_finals_by_team import plot_titles_finals_by_team
from charts.t3ch_playoff_appearances_wins import plot_playoff_appearances_wins
from charts.t3ch_head_to_head_win import plot_head_to_head_win
from charts.t3ch_team_win_pct import plot_team_win_pct
from charts.t3ch_team_win_pct_trend import plot_team_win_pct_trend

def render(filtered_match_df):

    # Season filter specific to this tab
    tab_selected_years = season_filter(
        filtered_match_df,
        label="Select Season(s) for Team Analysis",
        key="team_tab_season_filter"
    )

    tab_match_df = filtered_match_df[
        filtered_match_df["year"].isin(tab_selected_years)
    ]

    st.divider()

    st.subheader("IPL Titles and Final Appearances by Team")
    titles_df = get_titles_finals_by_team(tab_match_df)
    fig = plot_titles_finals_by_team(titles_df)
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("Playoff Appearances and Wins by Team")
    playoff_df = get_playoff_appearances_wins_by_team(tab_match_df)
    fig2 = plot_playoff_appearances_wins(playoff_df)
    st.plotly_chart(fig2, width="stretch")

    st.divider()

    st.subheader("Head-to-Head Win % Matrix")
    win_pct, wins, matches = get_head_to_head_win(tab_match_df) # type: ignore
    fig3 = plot_head_to_head_win(win_pct, wins, matches)
    st.plotly_chart(fig3, width="stretch")

    st.divider()

    st.subheader("Team Win %")
    win_df = get_team_win_pct(tab_match_df)
    fig4 = plot_team_win_pct(win_df)
    st.plotly_chart(fig4, width="stretch")

    st.divider()

    st.subheader("Team Performance Trend by Season")
    trend_df = get_team_win_pct_by_season(tab_match_df)
    teams = sorted(trend_df["team"].unique())
    selected_teams = st.multiselect(
        "Select Teams",
        options=teams,
        default=teams[:4]  # default few teams for readability
    )
    fig5 = plot_team_win_pct_trend(trend_df, selected_teams)
    st.plotly_chart(fig5, width="stretch")