import plotly.graph_objects as go


def plot_batter_boundaries_by_year(bd_df, player_name):

    if bd_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    years = bd_df["year"].astype(str)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=years,
            y=bd_df["fours"],
            name="4s",
            marker_color="#4C72B0",
            text=bd_df["fours"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>4s: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=bd_df["sixes"],
            name="6s",
            marker_color="#DD8452",
            text=bd_df["sixes"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>6s: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=bd_df["combined"],
            name="Combined",
            marker_color="#55A868",
            text=bd_df["combined"],
            texttemplate="%{text}",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>Combined boundaries: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Boundaries by season — {player_name}",
        barmode="group",
        xaxis=dict(title="Season", tickangle=45),
        yaxis=dict(title="Count"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, len(bd_df) * 40),
        margin=dict(t=120),
    )

    return fig
