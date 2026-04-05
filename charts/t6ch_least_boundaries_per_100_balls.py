import plotly.graph_objects as go


def plot_least_boundaries_per_100_balls(boundaries_df, top_n):
    
    if boundaries_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = boundaries_df["bowler"]

    # Total 4s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["total_4s_per_100"],
            y=bowlers,
            orientation="h",
            name="Total 4s/100 Balls",
            offsetgroup=0,
            marker_color="#1f77b4",
            text=boundaries_df["total_4s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total 4s/100 Balls: %{x:.2f}<br>Total 6s/100 Balls: %{customdata:.2f}<extra></extra>",
            customdata=boundaries_df["total_6s_per_100"],
        )
    )

    # Total 6s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["total_6s_per_100"],
            y=bowlers,
            orientation="h",
            name="Total 6s/100 Balls",
            offsetgroup=0,
            marker_color="#aec7e8",
            text=boundaries_df["total_6s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>Total 4s/100 Balls: %{customdata:.2f}<br>Total 6s/100 Balls: %{x:.2f}<extra></extra>",
            customdata=boundaries_df["total_4s_per_100"],
        )
    )

    # PowerPlay 4s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["PowerPlay_4s_per_100"],
            y=bowlers,
            orientation="h",
            name="PowerPlay 4s/100 Balls",
            offsetgroup=1,
            marker_color="#ff7f0e",
            text=boundaries_df["PowerPlay_4s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay 4s/100 Balls: %{x:.2f}<br>PowerPlay 6s/100 Balls: %{customdata:.2f}<extra></extra>",
            customdata=boundaries_df["PowerPlay_6s_per_100"],
        )
    )

    # PowerPlay 6s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["PowerPlay_6s_per_100"],
            y=bowlers,
            orientation="h",
            name="PowerPlay 6s/100 Balls",
            offsetgroup=1,
            marker_color="#ffbb78",
            text=boundaries_df["PowerPlay_6s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>PowerPlay 4s/100 Balls: %{customdata:.2f}<br>PowerPlay 6s/100 Balls: %{x:.2f}<extra></extra>",
            customdata=boundaries_df["PowerPlay_4s_per_100"],
        )
    )

    # Mid 4s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Mid_4s_per_100"],
            y=bowlers,
            orientation="h",
            name="Mid 4s/100 Balls",
            offsetgroup=1,
            marker_color="#2ca02c",
            text=boundaries_df["Mid_4s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid 4s/100 Balls: %{x:.2f}<br>Mid 6s/100 Balls: %{customdata:.2f}<extra></extra>",
            customdata=boundaries_df["Mid_6s_per_100"],
        )
    )

    # Mid 6s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Mid_6s_per_100"],
            y=bowlers,
            orientation="h",
            name="Mid 6s/100 Balls",
            offsetgroup=1,
            marker_color="#98df8a",
            text=boundaries_df["Mid_6s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>Mid 4s/100 Balls: %{customdata:.2f}<br>Mid 6s/100 Balls: %{x:.2f}<extra></extra>",
            customdata=boundaries_df["Mid_4s_per_100"],
        )
    )

    # Death 4s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Death_4s_per_100"],
            y=bowlers,
            orientation="h",
            name="Death 4s/100 Balls",
            offsetgroup=1,
            marker_color="#d62728",
            text=boundaries_df["Death_4s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death 4s/100 Balls: %{x:.2f}<br>Death 6s/100 Balls: %{customdata:.2f}<extra></extra>",
            customdata=boundaries_df["Death_6s_per_100"],
        )
    )

    # Death 6s per 100 balls
    fig.add_trace(
        go.Bar(
            x=boundaries_df["Death_6s_per_100"],
            y=bowlers,
            orientation="h",
            name="Death 6s/100 Balls",
            offsetgroup=1,
            marker_color="#ff9896",
            text=boundaries_df["Death_6s_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="black"),
            hovertemplate="Bowler: %{y}<br>Death 4s/100 Balls: %{customdata:.2f}<br>Death 6s/100 Balls: %{x:.2f}<extra></extra>",
            customdata=boundaries_df["Death_4s_per_100"],
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Least Boundary Giving Bowlers per 100 Balls (Total and Phases Split by 4s/6s)",
        barmode="stack",
        xaxis=dict(title="Boundaries per 100 Balls"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="right", x=0.99),
        height=max(450, top_n * 45),
    )

    return fig