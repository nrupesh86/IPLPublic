import plotly.graph_objects as go

def plot_titles_finals_by_team(df):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["team"],
            y=df["final_appearances"],
            name="Final Appearances",
            marker_color="#4C72B0",
            text=df["final_appearances"],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["team"],
            y=df["titles"],
            name="Titles Won",
            marker_color="#2CA02C",
            text=df["titles"],
            textposition="inside"
        )
    )

    fig.update_layout(
        barmode="group",
        title="Final Appearances vs Titles",
        xaxis=dict(
            title="Team",
            tickangle=45
        ),
        yaxis=dict(
            title="Count"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=100),
        height=550
    )

    return fig