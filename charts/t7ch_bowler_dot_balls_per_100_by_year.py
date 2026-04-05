import plotly.graph_objects as go


def plot_bowler_dot_balls_per_100_by_year(dot_df, bowler):
    if dot_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    dot_df = dot_df.copy()
    if "PowerPlay_dot_balls_per_100" not in dot_df.columns:
        dot_df["PowerPlay_dot_balls_per_100"] = dot_df.get("PowerPlay", 0)
    if "Mid_dot_balls_per_100" not in dot_df.columns:
        dot_df["Mid_dot_balls_per_100"] = dot_df.get("Mid", 0)
    if "Death_dot_balls_per_100" not in dot_df.columns:
        dot_df["Death_dot_balls_per_100"] = dot_df.get("Death", 0)

    if "total_balls" not in dot_df.columns:
        dot_df["total_balls"] = 0
    if "total_dot_balls" not in dot_df.columns:
        dot_df["total_dot_balls"] = 0
    if "PowerPlay_balls" not in dot_df.columns:
        dot_df["PowerPlay_balls"] = 0
    if "Mid_balls" not in dot_df.columns:
        dot_df["Mid_balls"] = 0
    if "Death_balls" not in dot_df.columns:
        dot_df["Death_balls"] = 0
    if "PowerPlay_dot_balls" not in dot_df.columns:
        dot_df["PowerPlay_dot_balls"] = 0
    if "Mid_dot_balls" not in dot_df.columns:
        dot_df["Mid_dot_balls"] = 0
    if "Death_dot_balls" not in dot_df.columns:
        dot_df["Death_dot_balls"] = 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["total_dot_balls_per_100"],
            name="Total Dot Balls/100 Balls",
            offsetgroup="Total Dot Balls/100 Balls",
            marker_color="#1f77b4",
            text=dot_df["total_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=dot_df[["total_balls", "total_dot_balls"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Total Dot Balls/100 Balls: %{y:.2f}<br>Total Balls: %{customdata[0]:.0f}<br>Total Dot Balls: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["PowerPlay_dot_balls_per_100"],
            name="PowerPlay Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#ff7f0e",
            text=dot_df["PowerPlay_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=dot_df[["PowerPlay_balls", "PowerPlay_dot_balls"]].to_numpy(),
            hovertemplate="Year: %{x}<br>PowerPlay Dot Balls/100 Balls: %{y:.2f}<br>PowerPlay Balls: %{customdata[0]:.0f}<br>PowerPlay Dot Balls: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["Mid_dot_balls_per_100"],
            name="Mid Overs Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#2ca02c",
            text=dot_df["Mid_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=dot_df[["Mid_balls", "Mid_dot_balls"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Mid Overs Dot Balls/100 Balls: %{y:.2f}<br>Mid Overs Balls: %{customdata[0]:.0f}<br>Mid Overs Dot Balls: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["Death_dot_balls_per_100"],
            name="Death Overs Dot Balls/100 Balls",
            offsetgroup="Phase Dot Balls/100 Balls",
            marker_color="#d62728",
            text=dot_df["Death_dot_balls_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=dot_df[["Death_balls", "Death_dot_balls"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Death Overs Dot Balls/100 Balls: %{y:.2f}<br>Death Overs Balls: %{customdata[0]:.0f}<br>Death Overs Dot Balls: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Dot Balls per 100 Balls by Season (Total + Phase)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Dot Balls / 100 Balls"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
