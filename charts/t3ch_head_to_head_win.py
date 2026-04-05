import plotly.graph_objects as go
import numpy as np

def plot_head_to_head_win(win_pct, wins, matches):

    # stack wins + matches into customdata
    customdata = np.dstack((wins.values, matches.values))

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=win_pct.values,
            x=win_pct.columns,
            y=win_pct.index,
            colorscale="RdYlGn",
            zmin=0,
            zmax=100,
            colorbar=dict(title="Win %"),
            text=win_pct.values,
            texttemplate="%{text:.1f}",
            customdata=customdata,
            hovertemplate=(
                "Team: %{y}<br>"
                "Opponent: %{x}<br>"
                "Win %: %{z:.1f}%<br>"
                "Wins: %{customdata[0]}<br>"
                "Matches: %{customdata[1]}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Head-to-Head Win % (Team vs Team)",
        xaxis=dict(tickangle=45),
        yaxis=dict(autorange="reversed"),
        height=700
    )

    return fig