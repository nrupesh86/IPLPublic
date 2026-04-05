import plotly.graph_objects as go


def plot_bowler_economy_by_year(econ_df, bowler):
    if econ_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    econ_df = econ_df.copy()
    if "total_economy" not in econ_df.columns:
        econ_df["total_economy"] = econ_df[["PowerPlay", "Mid", "Death"]].mean(axis=1)
    if "PowerPlay_economy" not in econ_df.columns:
        econ_df["PowerPlay_economy"] = econ_df.get("PowerPlay", 0)
    if "Mid_economy" not in econ_df.columns:
        econ_df["Mid_economy"] = econ_df.get("Mid", 0)
    if "Death_economy" not in econ_df.columns:
        econ_df["Death_economy"] = econ_df.get("Death", 0)

    if "total_balls" not in econ_df.columns:
        econ_df["total_balls"] = 0
    if "total_runs" not in econ_df.columns:
        econ_df["total_runs"] = 0
    if "PowerPlay_balls" not in econ_df.columns:
        econ_df["PowerPlay_balls"] = 0
    if "Mid_balls" not in econ_df.columns:
        econ_df["Mid_balls"] = 0
    if "Death_balls" not in econ_df.columns:
        econ_df["Death_balls"] = 0
    if "PowerPlay_runs" not in econ_df.columns:
        econ_df["PowerPlay_runs"] = 0
    if "Mid_runs" not in econ_df.columns:
        econ_df["Mid_runs"] = 0
    if "Death_runs" not in econ_df.columns:
        econ_df["Death_runs"] = 0

    econ_df["total_overs"] = (econ_df["total_balls"] / 6).round(2)
    econ_df["PowerPlay_overs"] = (econ_df["PowerPlay_balls"] / 6).round(2)
    econ_df["Mid_overs"] = (econ_df["Mid_balls"] / 6).round(2)
    econ_df["Death_overs"] = (econ_df["Death_balls"] / 6).round(2)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=econ_df["year"],
            y=econ_df["total_economy"],
            name="Total Economy",
            offsetgroup="Total Economy",
            marker_color="#1f77b4",
            text=econ_df["total_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=econ_df[["total_overs", "total_runs"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Total Economy: %{y:.2f}<br>Total Overs: %{customdata[0]:.2f}<br>Total Runs: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=econ_df["year"],
            y=econ_df["PowerPlay_economy"],
            name="PowerPlay Economy",
            offsetgroup="Phase Economy",
            marker_color="#ff7f0e",
            text=econ_df["PowerPlay_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=econ_df[["PowerPlay_overs", "PowerPlay_runs"]].to_numpy(),
            hovertemplate="Year: %{x}<br>PowerPlay Economy: %{y:.2f}<br>PowerPlay Overs: %{customdata[0]:.2f}<br>PowerPlay Runs: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=econ_df["year"],
            y=econ_df["Mid_economy"],
            name="Mid Economy",
            offsetgroup="Phase Economy",
            marker_color="#2ca02c",
            text=econ_df["Mid_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=econ_df[["Mid_overs", "Mid_runs"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Mid Economy: %{y:.2f}<br>Mid Overs: %{customdata[0]:.2f}<br>Mid Runs: %{customdata[1]:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=econ_df["year"],
            y=econ_df["Death_economy"],
            name="Death Economy",
            offsetgroup="Phase Economy",
            marker_color="#d62728",
            text=econ_df["Death_economy"].round(2),
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=econ_df[["Death_overs", "Death_runs"]].to_numpy(),
            hovertemplate="Year: %{x}<br>Death Economy: %{y:.2f}<br>Death Overs: %{customdata[0]:.2f}<br>Death Runs: %{customdata[1]:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Economy by Season (Total + Phase)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Economy"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
