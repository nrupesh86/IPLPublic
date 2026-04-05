import plotly.graph_objects as go

def plot_team_win_pct_trend(df, selected_teams):

    fig = go.Figure()

    for team in selected_teams:
        team_df = df[df["team"] == team]

        fig.add_trace(
            go.Scatter(
                x=team_df["year"],
                y=team_df["win_pct"],
                mode="lines+markers",
                name=team,
                hovertemplate=(
                    "Team: " + team +
                    "<br>Year: %{x}" +
                    "<br>Win %: %{y:.1f}%<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="Team Performance Trend (Win % by Season)",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Win %"),
        height=550,
        legend=dict(
            orientation="h",
            y=1.15
        )
    )

    return fig