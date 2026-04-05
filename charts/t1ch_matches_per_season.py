import plotly.graph_objects as go

def plot_matches_per_season(filtered_match_df):

    matches_per_year = (
        filtered_match_df
        .groupby("year")["match_id"]
        .count()
        .reset_index(name="matches")
        .sort_values("year")
    )

    max_value = matches_per_year["matches"].max()

    # Determine text position dynamically
    text_positions = [
        "inside" if val > max_value * 0.05 else "outside"
        for val in matches_per_year["matches"]
    ]

    text_colors = [
        "white" for val in matches_per_year["matches"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=matches_per_year["year"],
            y=matches_per_year["matches"],
            marker_color="#4C72B0",
            text=matches_per_year["matches"],
            textposition=text_positions,
            textfont=dict(color=text_colors),
            hovertemplate="Season: %{x}<br>Matches: %{y}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Matches per Season",
        xaxis=dict(
            title="Season",
            tickangle=270
        ),
        yaxis=dict(title="Number of Matches"),
        height=500
    )

    return fig