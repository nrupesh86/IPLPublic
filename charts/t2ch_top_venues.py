from enum import auto

import plotly.graph_objects as go

def plot_top_venues(filtered_match_df, top_n):

    matches_per_venue = (
        filtered_match_df
        .groupby("venue")["match_id"]
        .count()
        .reset_index(name="matches")
        .sort_values("matches", ascending=False)
        .head(top_n)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=matches_per_venue["venue"],
            x=matches_per_venue["matches"],
            orientation="h",
            marker_color="#4C72B0",
            text=matches_per_venue["matches"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            hovertemplate="Venue: %{y}<br>Matches: %{x}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Venues by Matches",
        xaxis=dict(title="Number of Matches"),
        yaxis=dict(
            title="Venue",
            autorange="reversed"),
        height=max(400, top_n*35)
    )

    return fig