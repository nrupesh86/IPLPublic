import plotly.graph_objects as go


def plot_top_boundaries(boundary_df, top_n, min_runs, sort_by_label):

    if boundary_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    customdata = list(
        zip(
            boundary_df["fours"],
            boundary_df["sixes"],
            boundary_df["combined"],
            boundary_df["total_runs"],
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=boundary_df["player"],
            x=boundary_df["fours"],
            orientation="h",
            name="4s",
            marker_color="#4C72B0",
            customdata=customdata,
            hovertemplate=(
                "Player: %{y}<br>"
                "4s: %{customdata[0]}<br>"
                "6s: %{customdata[1]}<br>"
                "Combined: %{customdata[2]}<br>"
                "Runs: %{customdata[3]:,}<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            y=boundary_df["player"],
            x=boundary_df["sixes"],
            orientation="h",
            name="6s",
            marker_color="#DD8452",
            customdata=customdata,
            hovertemplate=(
                "Player: %{y}<br>"
                "4s: %{customdata[0]}<br>"
                "6s: %{customdata[1]}<br>"
                "Combined: %{customdata[2]}<br>"
                "Runs: %{customdata[3]:,}<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            y=boundary_df["player"],
            x=boundary_df["combined"],
            orientation="h",
            name="Combined",
            marker_color="#55A868",
            customdata=customdata,
            hovertemplate=(
                "Player: %{y}<br>"
                "4s: %{customdata[0]}<br>"
                "6s: %{customdata[1]}<br>"
                "Combined: %{customdata[2]}<br>"
                "Runs: %{customdata[3]:,}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=(
            f"Top {top_n} Boundary Hitters (min. {min_runs:,} runs, sorted by {sort_by_label})"
        ),
        barmode="group",
        xaxis=dict(title="Boundary count"),
        yaxis=dict(title="Player", autorange="reversed"),
        height=max(400, top_n * 45),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
