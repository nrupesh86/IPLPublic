import plotly.graph_objects as go


def plot_top_wickets_per_100_balls(wickets_df, top_n):
    
    if wickets_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = wickets_df["bowler"]

    # Total wickets per 100 balls bar
    fig.add_trace(
        go.Bar(
            x=wickets_df["total_wickets_per_100"],
            y=bowlers,
            orientation="h",
            name="Total Wickets/100 Balls",
            offsetgroup="Total Wickets/100 Balls",
            marker_color="#1f77b4",
            text=wickets_df["total_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total Wickets/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # PowerPlay wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wickets_df["PowerPlay_wickets_per_100"],
            y=bowlers,
            orientation="h",
            name="PowerPlay Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#ff7f0e",
            text=wickets_df["PowerPlay_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay Wickets/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # Mid wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wickets_df["Mid_wickets_per_100"],
            y=bowlers,
            orientation="h",
            name="Mid Overs Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#2ca02c",
            text=wickets_df["Mid_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid Overs Wickets/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # Death wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wickets_df["Death_wickets_per_100"],
            y=bowlers,
            orientation="h",
            name="Death Overs Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#d62728",
            text=wickets_df["Death_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death Overs Wickets/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Wicket Takers per 100 Balls",
        barmode="stack",
        xaxis=dict(title="Wickets per 100 Balls"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig