import plotly.graph_objects as go


def plot_batter_runs_by_year(runs_df, player_name):

    if runs_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    years = runs_df["year"].astype(str)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=years,
            y=runs_df["boundary_runs"],
            name="Boundary runs",
            offsetgroup="boundaries_cluster",
            legendgroup="boundaries_cluster",
            marker_color="#4C72B0",
            text=runs_df["boundary_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=runs_df["total_runs"],
            hovertemplate="Year: %{x}<br>Boundary runs: %{y}<br>Season runs: %{customdata}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=runs_df["non_boundary_runs"],
            name="Non-boundary runs",
            offsetgroup="boundaries_cluster",
            legendgroup="boundaries_cluster",
            marker_color="#55A868",
            text=runs_df["non_boundary_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=runs_df["total_runs"],
            hovertemplate="Year: %{x}<br>Non-boundary runs: %{y}<br>Season runs: %{customdata}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=runs_df["powerplay_runs"],
            name="Powerplay runs",
            offsetgroup="phase_cluster",
            legendgroup="phase_cluster",
            marker_color="#DD8452",
            text=runs_df["powerplay_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=runs_df["total_runs"],
            hovertemplate="Year: %{x}<br>Powerplay runs: %{y}<br>Season runs: %{customdata}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=runs_df["non_powerplay_runs"],
            name="Non-powerplay runs",
            offsetgroup="phase_cluster",
            legendgroup="phase_cluster",
            marker_color="#C44E52",
            text=runs_df["non_powerplay_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=runs_df["total_runs"],
            hovertemplate="Year: %{x}<br>Non-powerplay runs: %{y}<br>Season runs: %{customdata}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Runs by season — {player_name}",
        barmode="stack",
        xaxis=dict(title="Season", tickangle=45),
        yaxis=dict(title="Runs"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, len(runs_df) * 40),
        margin=dict(t=120),
    )

    return fig
