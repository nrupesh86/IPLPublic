import plotly.graph_objects as go

def plot_toss_impact_per_season(toss_df):

    fig = go.Figure()

    toss_df = toss_df.sort_values("year")

    # Win %
    fig.add_trace(
        go.Bar(
            x=toss_df["year"],
            y=toss_df["win_pct"],
            name="Toss Win → Match Win %",
            marker_color="#2CA02C",
            text=toss_df["win_pct"],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Season: %{x}<br>Win %: %{y:.1f}%<extra></extra>"
        )
    )

    # Loss %
    fig.add_trace(
        go.Bar(
            x=toss_df["year"],
            y=toss_df["loss_pct"],
            name="Toss Win → Match Loss %",
            marker_color="#E24A33",
            text=toss_df["loss_pct"],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Season: %{x}<br>Loss %: %{y:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Toss Impact on Match Outcome (%)",
        xaxis=dict(title="Season"),
        yaxis=dict(
            title="Percentage",
            range=[0, 100]
        ),
        legend=dict(x=0.01, y=0.99),
        height=500
    )

    return fig