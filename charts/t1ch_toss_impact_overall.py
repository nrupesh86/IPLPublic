import plotly.graph_objects as go

def plot_toss_impact_overall(toss_impact_overall_dict):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=["Overall Toss Impact"],
            x=[toss_impact_overall_dict["win_pct"]],
            name="Toss Win → Match Win %",
            orientation="h",
            marker_color="#2CA02C",
            text=[toss_impact_overall_dict["win_pct"]],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Win %: %{x:.1f}%<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            y=["Overall Toss Impact"],
            x=[toss_impact_overall_dict["loss_pct"]],
            name="Toss Win → Match Loss %",
            orientation="h",
            marker_color="#E24A33",
            text=[toss_impact_overall_dict["loss_pct"]],
            texttemplate="%{text:.1f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Loss %: %{x:.1f}%<extra></extra>"
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Overall Toss Impact (%)",
        xaxis=dict(
            title="Percentage",
            range=[0, 100]
        ),
        yaxis=dict(showticklabels=False),
        height=250,
        legend=dict(orientation="h", y=1.15)
    )

    return fig