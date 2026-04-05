import plotly.graph_objects as go

def plot_innings_win_per_season(innings_df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=innings_df["year"],
            y=innings_df["bat_first_pct"],
            name="Batting First Wins %",
            marker_color="#4C72B0",
            text=innings_df["bat_first_pct"],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Season: %{x}<br>Bat First Win %: %{y:.1f}%<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            x=innings_df["year"],
            y=innings_df["bowl_first_pct"],
            name="Bowling First Wins %",
            marker_color="#E24A33",
            text=innings_df["bowl_first_pct"],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Season: %{x}<br>Bowl First Win %: %{y:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Match Outcome by Innings Choice (%)",
        xaxis=dict(title="Season", tickangle=270),
        yaxis=dict(title="Percentage", range=[0, 100]),
        height=500,
        legend=dict(x=0.01, y=0.99)
    )

    return fig