import plotly.graph_objects as go


def plot_batter_avg_sr_by_year(avg_sr_df, player_name):

    plot_df = avg_sr_df.dropna(subset=["average", "strike_rate"], how="all")
    plot_df = plot_df[
        plot_df["average"].notna() & plot_df["strike_rate"].notna()
    ]
    if plot_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot (need dismissals and balls faced per season)")
        return fig

    amax = plot_df["average"].max()
    smax = plot_df["strike_rate"].max()
    if amax <= 0 or smax <= 0:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    years = plot_df["year"].astype(str)
    avg_seg = plot_df["average"] / amax * 100
    sr_seg = plot_df["strike_rate"] / smax * 100

    customdata = list(
        zip(plot_df["average"], plot_df["strike_rate"], plot_df["total_runs"])
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=years,
            y=avg_seg,
            name="Average (vs chart max)",
            marker_color="#DD8452",
            customdata=customdata,
            hovertemplate=(
                "Year: %{x}<br>"
                "Average: %{customdata[0]:.2f}<br>"
                "Strike rate: %{customdata[1]:.2f}<br>"
                "Runs: %{customdata[2]:,}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=sr_seg,
            name="Strike rate (vs chart max)",
            marker_color="#4C72B0",
            customdata=customdata,
            hovertemplate=(
                "Year: %{x}<br>"
                "Average: %{customdata[0]:.2f}<br>"
                "Strike rate: %{customdata[1]:.2f}<br>"
                "Runs: %{customdata[2]:,}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"Batting average & strike rate by season — {player_name}",
        barmode="group",
        xaxis=dict(title="Season", tickangle=45),
        yaxis=dict(title="Index (each metric ÷ its max in this chart; 0–100)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, len(plot_df) * 45),
        margin=dict(t=120),
    )

    return fig
