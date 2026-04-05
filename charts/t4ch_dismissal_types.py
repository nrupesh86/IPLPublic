import plotly.graph_objects as go


def plot_dismissal_types(dismissal_long_df, top_n, min_runs):

    if dismissal_long_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    fig = go.Figure()

    for kind in dismissal_long_df["wicket_kind_group"].dropna().unique().tolist():
        kind_df = dismissal_long_df[dismissal_long_df["wicket_kind_group"] == kind]
        fig.add_trace(
            go.Bar(
                x=kind_df["player"],
                y=kind_df["dismissals"],
                name=str(kind),
                text=kind_df["dismissals"],
                texttemplate="%{text}",
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white"),
                customdata=list(
                    zip(kind_df["total_dismissals"], kind_df["total_runs"])
                ),
                hovertemplate=(
                    "Player: %{x}<br>"
                    "Dismissal type: " + str(kind) + "<br>"
                    "Dismissals: %{y}<br>"
                    "Total dismissals: %{customdata[0]}<br>"
                    "Runs: %{customdata[1]:,}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=f"Top {top_n} Batters by Dismissal Types (min. {min_runs:,} runs)",
        barmode="group",
        xaxis=dict(tickangle=45, title="Batter"),
        yaxis=dict(title="Dismissals"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=120),
        height=max(550, top_n * 45),
    )

    return fig

