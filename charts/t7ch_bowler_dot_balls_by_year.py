import plotly.graph_objects as go


def plot_bowler_dot_balls_by_year(dot_df, bowler):
    if dot_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    dot_df = dot_df.copy()
    if "total_dot_balls" not in dot_df.columns:
        dot_df["total_dot_balls"] = dot_df[["PowerPlay", "Mid", "Death"]].sum(axis=1)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["total_dot_balls"],
            name="Total Dot Balls",
            offsetgroup="Total Dot Balls",
            marker_color="#1f77b4",
            text=dot_df["total_dot_balls"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>Total Dot Balls: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["PowerPlay"],
            name="PowerPlay Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#ff7f0e",
            text=dot_df["PowerPlay"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>PowerPlay Dot Balls: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["Mid"],
            name="Mid Overs Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#2ca02c",
            text=dot_df["Mid"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>Mid Overs Dot Balls: %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dot_df["year"],
            y=dot_df["Death"],
            name="Death Overs Dot Balls",
            offsetgroup="Phase Dot Balls",
            marker_color="#d62728",
            text=dot_df["Death"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Year: %{x}<br>Death Overs Dot Balls: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Dot Balls per Season (Total + Phase)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Dot Balls"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
