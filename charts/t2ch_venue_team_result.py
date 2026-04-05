import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import math

def plot_venue_team_results(summary_df):

    # Remove "Unknown" teams
    summary_df = summary_df[
        summary_df["team"].str.lower() != "unknown"
    ]

    venue_order = (
        summary_df
        .groupby("venue")["count"]
        .sum()
        .sort_values(ascending=False)
        .index
    )

    venues = venue_order

    cols = 1
    rows = math.ceil(len(venues) / cols)

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=venues,
        vertical_spacing=0.03
    )

    for i, venue in enumerate(venues):

        r = i // cols + 1
        c = i % cols + 1

        venue_df = summary_df[summary_df["venue"] == venue]

        pivot = (
            venue_df
            .pivot(index="team", columns="result", values="count")
            .fillna(0)
        )

        pivot["total"] = pivot.sum(axis=1)

        pivot["win_pct"] = pivot["Win"] / pivot["total"] * 100
        pivot["loss_pct"] = pivot["Loss"] / pivot["total"] * 100

        # Sort teams by win %
        # pivot = pivot.sort_values("win_pct", ascending=False)

        fig.add_trace(
            go.Bar(
                x=pivot.index,
                y=pivot["win_pct"],
                name="Wins",
                marker_color="#2CA02C",
                text=[f"{c} ({p:.0f}%)" for c, p in zip(pivot["Win"], pivot["win_pct"])],
                textposition="inside",
                showlegend=(i == 0)
            ),
            row=r, col=c
        )

        fig.add_trace(
            go.Bar(
                x=pivot.index,
                y=pivot["loss_pct"],
                name="Losses",
                marker_color="#E24A33",
                text=[f"{c} ({p:.0f}%)" for c, p in zip(pivot["Loss"], pivot["loss_pct"])],
                textposition="inside",
                showlegend=(i == 0)
            ),
            row=r, col=c
        )

        # Improve team label readability
        fig.update_xaxes(
            tickangle=45,
            row=r,
            col=c
        )

    fig.update_layout(
        barmode="stack",
        height=420*rows,
        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        )
    )

    return fig