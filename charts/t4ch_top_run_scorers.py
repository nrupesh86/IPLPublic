import plotly.graph_objects as go


def plot_top_run_scorers(scorers_df, top_n):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=scorers_df["player"],
            x=scorers_df["boundary_runs"],
            orientation="h",
            marker_color="#4C72B0",
            name="Boundary runs",
            offsetgroup="boundaries_cluster",
            legendgroup="boundaries_cluster",
            text=scorers_df["boundary_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            customdata=scorers_df["total_runs"],
            hovertemplate="Player: %{y}<br>Boundary runs: %{x}<br>Total runs: %{customdata}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            y=scorers_df["player"],
            x=scorers_df["non_boundary_runs"],
            orientation="h",
            marker_color="#55A868",
            name="Non-boundary runs",
            offsetgroup="boundaries_cluster",
            legendgroup="boundaries_cluster",
            text=scorers_df["non_boundary_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            customdata=scorers_df["total_runs"],
            hovertemplate="Player: %{y}<br>Non-boundary runs: %{x}<br>Total runs: %{customdata}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            y=scorers_df["player"],
            x=scorers_df["powerplay_runs"],
            orientation="h",
            marker_color="#DD8452",
            name="Powerplay runs",
            offsetgroup="phase_cluster",
            legendgroup="phase_cluster",
            text=scorers_df["powerplay_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            customdata=scorers_df["total_runs"],
            hovertemplate="Player: %{y}<br>Powerplay runs: %{x}<br>Total runs: %{customdata}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            y=scorers_df["player"],
            x=scorers_df["non_powerplay_runs"],
            orientation="h",
            marker_color="#C44E52",
            name="Non-powerplay runs",
            offsetgroup="phase_cluster",
            legendgroup="phase_cluster",
            text=scorers_df["non_powerplay_runs"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            customdata=scorers_df["total_runs"],
            hovertemplate="Player: %{y}<br>Non-powerplay runs: %{x}<br>Total runs: %{customdata}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Run Scorers",
        barmode="stack",
        xaxis=dict(title="Runs"),
        yaxis=dict(title="Player", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig
