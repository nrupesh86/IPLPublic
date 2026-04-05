import plotly.graph_objects as go


def plot_bowler_wickets_per_100_by_year(wk_df, bowler):
    if wk_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    wk_df = wk_df.copy()
    if "PowerPlay_wickets_per_100" not in wk_df.columns:
        wk_df["PowerPlay_wickets_per_100"] = wk_df.get("PowerPlay", 0)
    if "Mid_wickets_per_100" not in wk_df.columns:
        wk_df["Mid_wickets_per_100"] = wk_df.get("Mid", 0)
    if "Death_wickets_per_100" not in wk_df.columns:
        wk_df["Death_wickets_per_100"] = wk_df.get("Death", 0)
    if "total_balls" not in wk_df.columns:
        wk_df["total_balls"] = 0
    if "total_wickets" not in wk_df.columns:
        wk_df["total_wickets"] = 0
    if "PowerPlay_balls" not in wk_df.columns:
        wk_df["PowerPlay_balls"] = 0
    if "Mid_balls" not in wk_df.columns:
        wk_df["Mid_balls"] = 0
    if "Death_balls" not in wk_df.columns:
        wk_df["Death_balls"] = 0
    if "PowerPlay_wickets" not in wk_df.columns:
        wk_df["PowerPlay_wickets"] = 0
    if "Mid_wickets" not in wk_df.columns:
        wk_df["Mid_wickets"] = 0
    if "Death_wickets" not in wk_df.columns:
        wk_df["Death_wickets"] = 0

    fig = go.Figure()
    # Total wickets per 100 balls bar
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["total_wickets_per_100"],
            name="Total Wickets/100 Balls",
            offsetgroup="Total Wickets/100 Balls",
            marker_color="#1f77b4",
            text=wk_df["total_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=wk_df[["total_balls", "total_wickets"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Total Wickets/100 Balls: %{y:.2f}<br>Total Balls: %{customdata[0]:.0f}<br>Total Wickets: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    # PowerPlay wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["PowerPlay_wickets_per_100"],
            name="PowerPlay Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#ff7f0e",
            text=wk_df["PowerPlay_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=wk_df[["PowerPlay_balls", "PowerPlay_wickets"]].to_numpy(),
            hovertemplate="Year: %{x}<br>PowerPlay Wickets/100 Balls: %{y:.2f}<br>PowerPlay Balls: %{customdata[0]:.0f}<br>PowerPlay Wickets: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    # Mid wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["Mid_wickets_per_100"],
            name="Mid Overs Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#2ca02c",
            text=wk_df["Mid_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=wk_df[["Mid_balls", "Mid_wickets"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Mid Overs Wickets/100 Balls: %{y:.2f}<br>Mid Overs Balls: %{customdata[0]:.0f}<br>Mid Overs Wickets: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    # Death wickets per 100 balls
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["Death_wickets_per_100"],
            name="Death Overs Wickets/100 Balls",
            offsetgroup="Phase Wickets/100 Balls",
            marker_color="#d62728",
            text=wk_df["Death_wickets_per_100"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=wk_df[["Death_balls", "Death_wickets"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Death Overs Wickets/100 Balls: %{y:.2f}<br>Death Overs Balls: %{customdata[0]:.0f}<br>Death Overs Wickets: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Wickets per 100 Balls by Season",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Wickets per 100 Balls"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
