import plotly.graph_objects as go


def plot_bowler_boundaries_per_100_by_year(bound_df, bowler):
    if bound_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    bound_df = bound_df.copy()
    if "PowerPlay_boundaries_per_100" not in bound_df.columns:
        bound_df["PowerPlay_boundaries_per_100"] = bound_df.get("PowerPlay", 0)
    if "Mid_boundaries_per_100" not in bound_df.columns:
        bound_df["Mid_boundaries_per_100"] = bound_df.get("Mid", 0)
    if "Death_boundaries_per_100" not in bound_df.columns:
        bound_df["Death_boundaries_per_100"] = bound_df.get("Death", 0)

    if "total_balls" not in bound_df.columns:
        bound_df["total_balls"] = 0
    if "total_boundaries" not in bound_df.columns:
        bound_df["total_boundaries"] = 0
    if "PowerPlay_balls" not in bound_df.columns:
        bound_df["PowerPlay_balls"] = 0
    if "Mid_balls" not in bound_df.columns:
        bound_df["Mid_balls"] = 0
    if "Death_balls" not in bound_df.columns:
        bound_df["Death_balls"] = 0
    if "PowerPlay_boundaries" not in bound_df.columns:
        bound_df["PowerPlay_boundaries"] = 0
    if "Mid_boundaries" not in bound_df.columns:
        bound_df["Mid_boundaries"] = 0
    if "Death_boundaries" not in bound_df.columns:
        bound_df["Death_boundaries"] = 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=bound_df["year"],
            y=bound_df["total_boundaries_per_100"],
            name="Total Boundaries/100 Balls",
            offsetgroup="Total Boundaries/100 Balls",
            marker_color="#1f77b4",
            text=bound_df["total_boundaries_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=bound_df[["total_balls", "total_boundaries"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Total Boundaries/100 Balls: %{y:.2f}<br>Total Balls: %{customdata[0]:.0f}<br>Total Boundaries: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=bound_df["year"],
            y=bound_df["PowerPlay_boundaries_per_100"],
            name="PowerPlay Boundaries/100 Balls",
            offsetgroup="Phase Boundaries/100 Balls",
            marker_color="#ff7f0e",
            text=bound_df["PowerPlay_boundaries_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=bound_df[["PowerPlay_balls", "PowerPlay_boundaries"]].to_numpy(),
            hovertemplate="Year: %{x}<br>PowerPlay Boundaries/100 Balls: %{y:.2f}<br>PowerPlay Balls: %{customdata[0]:.0f}<br>PowerPlay Boundaries: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=bound_df["year"],
            y=bound_df["Mid_boundaries_per_100"],
            name="Mid Overs Boundaries/100 Balls",
            offsetgroup="Phase Boundaries/100 Balls",
            marker_color="#2ca02c",
            text=bound_df["Mid_boundaries_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=bound_df[["Mid_balls", "Mid_boundaries"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Mid Overs Boundaries/100 Balls: %{y:.2f}<br>Mid Overs Balls: %{customdata[0]:.0f}<br>Mid Overs Boundaries: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=bound_df["year"],
            y=bound_df["Death_boundaries_per_100"],
            name="Death Overs Boundaries/100 Balls",
            offsetgroup="Phase Boundaries/100 Balls",
            marker_color="#d62728",
            text=bound_df["Death_boundaries_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=bound_df[["Death_balls", "Death_boundaries"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Death Overs Boundaries/100 Balls: %{y:.2f}<br>Death Overs Balls: %{customdata[0]:.0f}<br>Death Overs Boundaries: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Boundaries Conceded per 100 Balls by Season (Total + Phase)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Boundaries / 100 Balls"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
