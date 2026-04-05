import plotly.graph_objects as go


def plot_bowler_wickets_by_year(wk_df, bowler):
    if wk_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    # Ensure total wickets exists; fallback to phase sum if missing
    if "total_wickets" not in wk_df.columns:
        wk_df = wk_df.copy()
        wk_df["total_wickets"] = wk_df[["PowerPlay", "Mid", "Death"]].sum(axis=1)

    fig = go.Figure()

    # Total wickets cluster
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["total_wickets"],
            name="Total Wickets",
            marker_color="#1f77b4",
            offsetgroup="Total",
            text=wk_df["total_wickets"],
            textposition="auto",
        )
    )

    # Phase split cluster (stacked phases)
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["PowerPlay"],
            name="PowerPlay",
            marker_color="#ff7f0e",
            offsetgroup="Phase",
            text=wk_df["PowerPlay"],
            textposition="inside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["Mid"],
            name="Mid",
            marker_color="#2ca02c",
            offsetgroup="Phase",
            text=wk_df["Mid"],
            textposition="inside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=wk_df["year"],
            y=wk_df["Death"],
            name="Death",
            marker_color="#d62728",
            offsetgroup="Phase",
            text=wk_df["Death"],
            textposition="inside",
        )
    )

    fig.update_layout(
        title=f"{bowler} - Wickets per Season (Total + Phase split)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Wickets"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
