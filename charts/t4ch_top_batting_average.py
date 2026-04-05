import plotly.graph_objects as go


def plot_top_batting_average(avg_df, top_n, min_runs, sort_by_label):

    amax = avg_df["average"].max()
    smax = avg_df["strike_rate"].max()
    if amax <= 0 or smax <= 0:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    avg_seg = avg_df["average"] / amax * 100
    sr_seg = avg_df["strike_rate"] / smax * 100

    customdata = list(
        zip(
            avg_df["average"],
            avg_df["strike_rate"],
            avg_df["total_runs"],
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=avg_df["player"],
            x=avg_seg,
            orientation="h",
            name="Average (vs chart max)",
            marker_color="#DD8452",
            customdata=customdata,
            hovertemplate=(
                "Player: %{y}<br>"
                "Average: %{customdata[0]:.2f}<br>"
                "Strike rate: %{customdata[1]:.2f}<br>"
                "Runs: %{customdata[2]:,}<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            y=avg_df["player"],
            x=sr_seg,
            orientation="h",
            name="Strike rate (vs chart max)",
            marker_color="#4C72B0",
            customdata=customdata,
            hovertemplate=(
                "Player: %{y}<br>"
                "Average: %{customdata[0]:.2f}<br>"
                "Strike rate: %{customdata[1]:.2f}<br>"
                "Runs: %{customdata[2]:,}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=(
            f"Top {top_n} Batting Average & Strike Rate "
            f"(min. {min_runs:,} runs, sorted by {sort_by_label})"
        ),
        barmode="group",
        xaxis=dict(
            title="Index (each metric ÷ its max in this chart; 0–100)",
        ),
        yaxis=dict(title="Player", autorange="reversed"),
        height=max(400, top_n * 40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
