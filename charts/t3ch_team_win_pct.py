import plotly.graph_objects as go

def plot_team_win_pct(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["team"],
            y=df["win_pct"],
            marker_color="#2CA02C",
            text=[
                f"{w:.1f}% ({m})"
                for w, m in zip(df["win_pct"], df["matches"])
            ],
            textposition="inside",
            hovertemplate=(
                "Team: %{x}<br>"
                "Win %: %{y:.1f}%<br>"
                "Matches: %{customdata}"
                "<extra></extra>"
            ),
            customdata=df["matches"]
        )
    )

    fig.update_layout(
        title="Team Win Percentage",
        xaxis=dict(tickangle=45),
        yaxis=dict(title="Win %"),
        height=550
    )

    return fig