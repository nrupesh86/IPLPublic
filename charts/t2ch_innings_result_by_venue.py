import plotly.graph_objects as go

def plot_innings_results_by_venue(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["venue"],
            y=df["bat_first_pct"],
            name="Batting First Win %",
            marker_color="#4C72B0",
            text=[
                f"{int(w)} ({p:.0f}%)"
                for w, p in zip(df["bat_first_wins"], df["bat_first_pct"])
            ],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["venue"],
            y=df["bowl_first_pct"],
            name="Bowling First Win %",
            marker_color="#E24A33",
            text=[
                f"{int(w)} ({p:.0f}%)"
                for w, p in zip(df["bowl_first_wins"], df["bowl_first_pct"])
            ],
            textposition="inside"
        )
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(
            title="Venue",
            tickangle=45
        ),
        yaxis=dict(
            title="Win %",
            range=[0,100]
        ),
        legend=dict(
            orientation="h",
            y=1.12,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=100),
        height=600
    )

    return fig