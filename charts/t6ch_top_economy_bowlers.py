import plotly.graph_objects as go


def plot_top_economy_bowlers(economy_df, top_n):

    if economy_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = economy_df["bowler"]

    # Total economy bar
    fig.add_trace(
        go.Bar(
            x=economy_df["total_economy"],
            y=bowlers,
            orientation="h",
            name="Total Economy",
            offsetgroup="Total Economy",
            marker_color="#1f77b4",
            text=economy_df["total_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total Economy: %{x:.2f}<extra></extra>",
        )
    )

    # PowerPlay economy
    fig.add_trace(
        go.Bar(
            x=economy_df["PowerPlay_economy"],
            y=bowlers,
            orientation="h",
            name="PowerPlay Economy",
            offsetgroup="Phase Economy",
            marker_color="#ff7f0e",
            text=economy_df["PowerPlay_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay Economy: %{x:.2f}<extra></extra>",
        )
    )

    # Mid economy
    fig.add_trace(
        go.Bar(
            x=economy_df["Mid_economy"],
            y=bowlers,
            orientation="h",
            name="Mid Economy",
            offsetgroup="Phase Economy",
            marker_color="#2ca02c",
            text=economy_df["Mid_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid Economy: %{x:.2f}<extra></extra>",
        )
    )

    # Death economy
    fig.add_trace(
        go.Bar(
            x=economy_df["Death_economy"],
            y=bowlers,
            orientation="h",
            name="Death Economy",
            offsetgroup="Phase Economy",
            marker_color="#d62728",
            text=economy_df["Death_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death Economy: %{x:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Economy Bowlers by Phase",
        barmode="stack",
        xaxis=dict(title="Economy Rate"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig