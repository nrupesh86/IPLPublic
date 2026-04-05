import pandas as pd

def get_innings_win_per_season(match_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates batting first vs bowling first win % per season.
    """

    df = match_df.copy()

    # Identify if batting first team won
    df["bat_first_win"] = df["match_won_by"] == df["team_1"]

    summary = (
        df.groupby("year")
        .agg(
            total_matches=("match_id", "count"),
            bat_first_wins=("bat_first_win", "sum")
        )
        .reset_index()
    )

    summary["bowl_first_wins"] = summary["total_matches"] - summary["bat_first_wins"]

    summary["bat_first_pct"] = (
        summary["bat_first_wins"] / summary["total_matches"]
    ) * 100

    summary["bowl_first_pct"] = (
        summary["bowl_first_wins"] / summary["total_matches"]
    ) * 100

    return summary.sort_values("year")

def get_innings_win_overall(match_df):
    """
    Calculates overall batting first vs bowling first win % across all seasons.
    """

    df = match_df.copy()

    # Did batting first team win?
    df["bat_first_win"] = df["match_won_by"] == df["team_1"]

    total_matches = len(df)
    bat_first_wins = df["bat_first_win"].sum()
    bowl_first_wins = total_matches - bat_first_wins

    bat_first_pct = (bat_first_wins / total_matches) * 100
    bowl_first_pct = (bowl_first_wins / total_matches) * 100

    return {
        "bat_first_pct": bat_first_pct,
        "bowl_first_pct": bowl_first_pct
    }