import plotly.graph_objects as go

def plot_toss_impact_by_venue(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["venue"],
            y=df["win_pct"],
            name="Toss Win → Match Win %",
            marker_color="#2CA02C",
            text=[
                f"{int(w)} ({p:.0f}%)"
                for w, p in zip(df["toss_win_match_win"], df["win_pct"])
            ],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["venue"],
            y=df["loss_pct"],
            name="Toss Win → Match Loss %",
            marker_color="#E24A33",
            text=[
                f"{int(w)} ({p:.0f}%)"
                for w, p in zip(df["toss_win_match_loss"], df["loss_pct"])
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
            title="Percentage",
            range=[0, 100]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=100),
        height=600
    )

    return fig