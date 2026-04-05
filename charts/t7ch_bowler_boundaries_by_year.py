import plotly.graph_objects as go


def plot_bowler_boundaries_by_year(bound_df, bowler):
    if bound_df.empty:
        fig = go.Figure(); fig.update_layout(title="No data to plot"); return fig

    if "total_boundaries" not in bound_df.columns:
        bound_df = bound_df.copy()
        bound_df["total_boundaries"] = bound_df[["PowerPlay", "Mid", "Death"]].sum(axis=1)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=bound_df["year"], y=bound_df["total_boundaries"], name="Total Boundaries", offsetgroup="Total", marker_color="#1f77b4", text=bound_df["total_boundaries"], textposition="auto"))
    fig.add_trace(go.Bar(x=bound_df["year"], y=bound_df["PowerPlay"], name="PowerPlay", offsetgroup="Phase", marker_color="#ff7f0e", text=bound_df["PowerPlay"], textposition="inside"))
    fig.add_trace(go.Bar(x=bound_df["year"], y=bound_df["Mid"], name="Mid", offsetgroup="Phase", marker_color="#2ca02c", text=bound_df["Mid"], textposition="inside"))
    fig.add_trace(go.Bar(x=bound_df["year"], y=bound_df["Death"], name="Death", offsetgroup="Phase", marker_color="#d62728", text=bound_df["Death"], textposition="inside"))

    fig.update_layout(
        title=f"{bowler} - Boundaries Conceded per Season (Total + Phase)",
        barmode="stack",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Boundaries"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
    )
    return fig
