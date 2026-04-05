import plotly.graph_objects as go


def plot_top_dot_ball_bowlers(dot_balls_df, top_n):
    
    if dot_balls_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    bowlers = dot_balls_df["bowler"]

    # Total dot balls bar
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["total_dot_balls"],
            y=bowlers,
            orientation="h",
            name="Total Dot Balls",
            offsetgroup="Total Dot Balls",
            marker_color="#1f77b4",
            text=dot_balls_df["total_dot_balls"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total Dot Balls: %{x}<extra></extra>",
        )
    )

    # PowerPlay dot balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["PowerPlay"],
            y=bowlers,
            orientation="h",
            name="PowerPlay Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#ff7f0e",
            text=dot_balls_df["PowerPlay"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay Dot Balls: %{x}<extra></extra>",
        )
    )

    # Mid dot balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["Mid"],
            y=bowlers,
            orientation="h",
            name="Mid Overs Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#2ca02c",
            text=dot_balls_df["Mid"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid Overs Dot Balls: %{x}<extra></extra>",
        )
    )

    # Death dot balls
    fig.add_trace(
        go.Bar(
            x=dot_balls_df["Death"],
            y=bowlers,
            orientation="h",
            name="Death Overs Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#d62728",
            text=dot_balls_df["Death"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death Overs Dot Balls: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Dot Ball Bowlers by Phase",
        barmode="stack",
        xaxis=dict(title="Dot Balls"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig
