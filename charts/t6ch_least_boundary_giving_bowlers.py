import plotly.graph_objects as go


def plot_least_boundary_giving_bowlers(boundaries_df, top_n):
    
    if boundaries_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = boundaries_df["bowler"]

    # Total boundaries - 4s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["total_fours"],
            y=bowlers,
            orientation="h",
            name="4s (Total)",
            offsetgroup="Total Boundaries",
            marker_color="#4C72B0",
            text=boundaries_df["total_fours"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total 4s: %{x}<extra></extra>",
        )
    )

    # Total boundaries - 6s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["total_sixes"],
            y=bowlers,
            orientation="h",
            name="6s (Total)",
            offsetgroup="Total Boundaries",
            marker_color="#1f77b4",
            text=boundaries_df["total_sixes"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total 6s: %{x}<extra></extra>",
        )
    )

    # PowerPlay - 4s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["PowerPlay_fours"],
            y=bowlers,
            orientation="h",
            name="4s (PowerPlay)",
            offsetgroup="Phase Boundaries",
            marker_color="#AEC7E8",
            text=boundaries_df["PowerPlay_fours"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>PowerPlay 4s: %{x}<extra></extra>",
        )
    )

    # PowerPlay - 6s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["PowerPlay_sixes"],
            y=bowlers,
            orientation="h",
            name="6s (PowerPlay)",
            offsetgroup="Phase Boundaries",
            marker_color="#1f77b4",
            text=boundaries_df["PowerPlay_sixes"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay 6s: %{x}<extra></extra>",
        )
    )

    # Mid - 4s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Mid_fours"],
            y=bowlers,
            orientation="h",
            name="4s (Mid)",
            offsetgroup="Phase Boundaries",
            marker_color="#98DF8A",
            text=boundaries_df["Mid_fours"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>Mid 4s: %{x}<extra></extra>",
        )
    )

    # Mid - 6s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Mid_sixes"],
            y=bowlers,
            orientation="h",
            name="6s (Mid)",
            offsetgroup="Phase Boundaries",
            marker_color="#2ca02c",
            text=boundaries_df["Mid_sixes"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid 6s: %{x}<extra></extra>",
        )
    )

    # Death - 4s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Death_fours"],
            y=bowlers,
            orientation="h",
            name="4s (Death)",
            offsetgroup="Phase Boundaries",
            marker_color="#FF9896",
            text=boundaries_df["Death_fours"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>Death 4s: %{x}<extra></extra>",
        )
    )

    # Death - 6s
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Death_sixes"],
            y=bowlers,
            orientation="h",
            name="6s (Death)",
            offsetgroup="Phase Boundaries",
            marker_color="#d62728",
            text=boundaries_df["Death_sixes"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death 6s: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Least Boundary Giving Bowlers by Phase",
        barmode="stack",
        xaxis=dict(title="Boundaries (4s & 6s)"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="right", x=0.99),
        height=max(450, top_n * 45),
    )

    return fig
