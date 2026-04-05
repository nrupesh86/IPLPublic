import plotly.graph_objects as go

def plot_players_per_season(players_per_season):

    players_per_season = players_per_season.sort_values("year")

    max_value = players_per_season["total_players"].max()

    text_positions = [
        "inside" if val > max_value * 0.15 else "outside"
        for val in players_per_season["total_players"]
    ]

    text_colors = [
        "white" for val in players_per_season["total_players"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=players_per_season["year"],
            y=players_per_season["total_players"],
            marker_color="#55A868",
            text=players_per_season["total_players"],
            textposition=text_positions,
            textfont=dict(color=text_colors),
            hovertemplate="Season: %{x}<br>Total Players: %{y}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Total Players per Season",
        xaxis=dict(
            title="Season"
        ),
        yaxis=dict(title="Total Players")
    )

    return fig