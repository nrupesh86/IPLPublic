import plotly.graph_objects as go

def plot_playoff_appearances_wins(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["team"],
            y=df["playoff_appearances"],
            name="Playoff Appearances",
            marker_color="#DD8452",
            text=df["playoff_appearances"],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["team"],
            y=df["playoff_wins"],
            name="Playoff Match Wins",
            marker_color="#2CA02C",
            text=df["playoff_wins"],
            textposition="inside"
        )
    )

    fig.update_layout(
        barmode="group",
        title="Playoff Appearances vs Playoff Match Wins",
        xaxis=dict(tickangle=45),
        yaxis=dict(title="Count"),
        legend=dict(
            orientation="h",
            y=1.1,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(t=120),
        height=550
    )

    return fig