import plotly.graph_objects as go

def plot_toss_decision_per_season(toss_decision_df):

    toss_decision_df = toss_decision_df.sort_values("year")

    fig = go.Figure()

    # ---- Bat First Line ----
    fig.add_trace(
        go.Scatter(
            x=toss_decision_df["year"],
            y=toss_decision_df["bat_pct"],
            name="Opted to Bat %",
            mode="lines+markers+text",
            line=dict(color="#4C72B0", width=3),
            marker=dict(size=8),
            text=[f"{v:.1f}%" for v in toss_decision_df["bat_pct"]],
            textposition="top center",
            hovertemplate="Season: %{x}<br>Bat First: %{y:.1f}%<extra></extra>"
        )
    )

    # ---- Field First Line ----
    fig.add_trace(
        go.Scatter(
            x=toss_decision_df["year"],
            y=toss_decision_df["field_pct"],
            name="Opted to Field %",
            mode="lines+markers+text",
            line=dict(color="#F2C14E", width=3),
            marker=dict(size=8),
            text=[f"{v:.1f}%" for v in toss_decision_df["field_pct"]],
            textposition="bottom center",
            hovertemplate="Season: %{x}<br>Field First: %{y:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        title="Toss Decision Pattern per Season (%)",
        xaxis=dict(title="Season", tickangle=270),
        yaxis=dict(
            title="Percentage",
            range=[0, 100]
        ),
        height=500,
        legend=dict(x=0.01, y=0.99)
    )

    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color="gray"
    )

    return fig