import plotly.graph_objects as go


def plot_top_dot_balls_per_100_balls(dot_balls_df, top_n):
    
    if dot_balls_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = dot_balls_df["bowler"]

    # Total dot balls per 100 balls bar
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["total_dot_balls_per_100"],
            y=bowlers,
            orientation="h",
            name="Total Dot Balls/100 Balls",
            offsetgroup="Total Dot Balls/100 Balls",
            marker_color="#1f77b4",
            text=dot_balls_df["total_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total Dot Balls/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # PowerPlay dot balls per 100 balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["PowerPlay_dot_balls_per_100"],
            y=bowlers,
            orientation="h",
            name="PowerPlay Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#ff7f0e",
            text=dot_balls_df["PowerPlay_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay Dot Balls/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # Mid dot balls per 100 balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["Mid_dot_balls_per_100"],
            y=bowlers,
            orientation="h",
            name="Mid Overs Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#2ca02c",
            text=dot_balls_df["Mid_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid Overs Dot Balls/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    # Death dot balls per 100 balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["Death_dot_balls_per_100"],
            y=bowlers,
            orientation="h",
            name="Death Overs Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#d62728",
            text=dot_balls_df["Death_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death Overs Dot Balls/100 Balls: %{x:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Dot Ball Bowlers per 100 Balls",
        barmode="stack",
        xaxis=dict(title="Dot Balls per 100 Balls"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig