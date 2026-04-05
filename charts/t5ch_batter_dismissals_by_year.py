import plotly.graph_objects as go


def plot_batter_dismissals_by_year(dis_long_df, player_name):

    if dis_long_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data to plot")
        return fig

    years_sorted = sorted(dis_long_df["year"].unique())
    x = [str(int(y)) for y in years_sorted]

    fig = go.Figure()

    for kind in dis_long_df["wicket_kind_group"].dropna().unique().tolist():
        kind_df = dis_long_df[dis_long_df["wicket_kind_group"] == kind]
        series = kind_df.set_index("year")["dismissals"]
        y_vals = [int(series.get(y, 0)) for y in years_sorted]

        fig.add_trace(
            go.Bar(
                x=x,
                y=y_vals,
                name=str(kind),
                hovertemplate=(
                    "Year: %{x}<br>"
                    f"Type: {kind}<br>"
                    "Dismissals: %{y}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=f"Dismissal types by season — {player_name}",
        barmode="stack",
        xaxis=dict(title="Season", tickangle=45),
        yaxis=dict(title="Dismissals"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, len(years_sorted) * 35),
        margin=dict(t=120),
    )

    return fig
