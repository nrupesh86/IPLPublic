import plotly.graph_objects as go


def plot_top_wicket_takers(wickets_df, top_n):
    
    fig = go.Figure()

    bowlers = wickets_df["bowler"]

    # Total wickets bar
    fig.add_trace(
        go.Bar(
            x=wickets_df["total_wickets"],
            y=bowlers,
            orientation="h",
            name="Total Wickets",
            offsetgroup="Total Wickets",
            marker_color="#1f77b4",
            text=wickets_df["total_wickets"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Total Wickets: %{x}<extra></extra>",
        )
    )

    # PowerPlay wickets
    pp_y = wickets_df["PowerPlay"]
    fig.add_trace(
        go.Bar(
            x=pp_y,
            y=bowlers,
            orientation="h",
            name="PowerPlay Wickets",
            offsetgroup="Phase Wickets",
            marker_color="#ff7f0e",
            text=wickets_df["PowerPlay"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>PowerPlay Wickets: %{x}<extra></extra>",
        )
    )

    # Mid wickets
    mid_y = wickets_df["Mid"]
    fig.add_trace(
        go.Bar(
            x=mid_y,
            y=bowlers,
            orientation="h",
            name="Mid Overs Wickets",
            offsetgroup="Phase Wickets",
            marker_color="#2ca02c",
            text=wickets_df["Mid"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Mid Overs Wickets: %{x}<extra></extra>",
        )
    )

    # Death wickets
    death_y = wickets_df["Death"]
    fig.add_trace(
        go.Bar(
            x=death_y,
            y=bowlers,
            orientation="h",
            name="Death Overs Wickets",
            offsetgroup="Phase Wickets",
            marker_color="#d62728",
            text=wickets_df["Death"],
            texttemplate="%{text}",
            textposition="auto",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate="Bowler: %{y}<br>Death Overs Wickets: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Wicket Takers by Phase",
        barmode="stack",
        xaxis=dict(title="Wickets"),
        yaxis=dict(title="Bowler", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=max(450, top_n * 45),
    )

    return fig