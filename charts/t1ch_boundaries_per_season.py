import plotly.graph_objects as go
import numpy as np

def plot_boundaries_per_season(boundaries_df):

    # -------- Dynamic Range Calculation (70% Scope Logic) --------
    min_avg = min(
        boundaries_df["avg_fours"].min(),
        boundaries_df["avg_sixes"].min()
    )

    max_avg = max(
        boundaries_df["avg_fours"].max(),
        boundaries_df["avg_sixes"].max()
    )

    data_range = max_avg - min_avg

    padding = data_range * 0.15

    lower_bound = min_avg - padding
    upper_bound = max_avg + padding

    # Expand total axis span so data occupies ~70%
    adjusted_upper = lower_bound + (upper_bound - lower_bound) / 0.7

    # -------- Figure --------
    fig = go.Figure()

    # ---- Bars ----
    fig.add_trace(
        go.Bar(
            x=boundaries_df["year"],
            y=boundaries_df["fours"],
            name="Total 4s",
            marker_color="#4C72B0",
            hovertemplate="Season: %{x}<br>Total 4s: %{y}<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            x=boundaries_df["year"],
            y=boundaries_df["sixes"],
            name="Total 6s",
            marker_color="#DD8452",
            hovertemplate="Season: %{x}<br>Total 6s: %{y}<extra></extra>"
        )
    )

    # ---- Lines ----
    fig.add_trace(
        go.Scatter(
            x=boundaries_df["year"],
            y=boundaries_df["avg_fours"],
            name="Avg 4s per Match",
            mode="lines+markers",
            line=dict(color="#2CA02C", width=3),
            yaxis="y2",
            hovertemplate="Season: %{x}<br>Avg 4s: %{y:.2f}<extra></extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=boundaries_df["year"],
            y=boundaries_df["avg_sixes"],
            name="Avg 6s per Match",
            mode="lines+markers",
            line=dict(color="#D62728", width=3),
            yaxis="y2",
            hovertemplate="Season: %{x}<br>Avg 6s: %{y:.2f}<extra></extra>"
        )
    )

    # ---- Layout ----
    fig.update_layout(
        barmode="group",
        title="Boundaries per Season (Totals & Averages)",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Total Boundaries"),
        yaxis2=dict(
            title="Average per Match",
            overlaying="y",
            side="right",
            range=[lower_bound, adjusted_upper],
            dtick=1  # integer ticks
        ),
        legend=dict(x=0.01, y=0.99),
        height=600
    )

    return fig