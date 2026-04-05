import plotly.graph_objects as go

def plot_innings_win_overall(innings_win_overall):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=["Overall"],
            x=[innings_win_overall["bat_first_pct"]],
            name="Batting First Wins %",
            orientation="h",
            marker_color="#4C72B0",
            text=[innings_win_overall["bat_first_pct"]],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bat First Win %: %{x:.1f}%<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            y=["Overall"],
            x=[innings_win_overall["bowl_first_pct"]],
            name="Bowling First Wins %",
            orientation="h",
            marker_color="#E24A33",
            text=[innings_win_overall["bowl_first_pct"]],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowl First Win %: %{x:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Overall Match Outcome by Innings Choice (%)",
        xaxis=dict(
            title="Percentage",
            range=[0, 100]
        ),
        yaxis=dict(showticklabels=False),
        height=250,
        legend=dict(orientation="h", y=1.15)
    )

    return fig