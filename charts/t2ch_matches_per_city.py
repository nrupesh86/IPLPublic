import plotly.graph_objects as go

def plot_matches_per_city(filtered_match_df, top_n):

    matches_by_city = (
        filtered_match_df
        .groupby("city")["match_id"]
        .count()
        .reset_index(name="matches")
        .sort_values("matches", ascending=False)
        .head(top_n)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=matches_by_city["city"],
            x=matches_by_city["matches"],
            orientation="h",
            marker_color="#DD8452",
            text=matches_by_city["matches"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            textangle=0,
            hovertemplate="City: %{y}<br>Matches: %{x}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Cities by Matches",
        xaxis=dict(title="Number of Matches"),
        yaxis=dict(
            title="City",
            autorange="reversed"
        ),
        height=max(400, top_n * 35)
    )

    return fig