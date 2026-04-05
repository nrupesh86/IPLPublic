import pandas as pd

def get_toss_impact_per_season(match_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates toss win to match win % per season.
    """

    df = match_df.copy()

    # Toss winner won match
    df["toss_win_match_win"] = df["toss_winner"] == df["match_won_by"]

    summary = (
        df.groupby("year")
        .agg(
            total_matches=("match_id", "count"),
            wins=("toss_win_match_win", "sum")
        )
        .reset_index()
    )

    summary["losses"] = summary["total_matches"] - summary["wins"]

    summary["win_pct"] = (summary["wins"] / summary["total_matches"]) * 100
    summary["loss_pct"] = (summary["losses"] / summary["total_matches"]) * 100

    return summary.sort_values("year")

def get_toss_impact_overall(match_df):
    """
    Calculates overall toss win to match win percentage across all seasons.
    """

    df = match_df.copy()

    df["toss_win_match_win"] = df["toss_winner"] == df["match_won_by"]

    total_matches = len(df)
    wins = df["toss_win_match_win"].sum()
    losses = total_matches - wins

    win_pct = (wins / total_matches) * 100
    loss_pct = (losses / total_matches) * 100

    return {
        "win_pct": win_pct,
        "loss_pct": loss_pct
    }

def get_toss_decision_per_season(match_df):
    """
    Returns toss decision % (bat vs field) per season.
    """

    df = match_df.copy()

    summary = (
        df.groupby(["year", "toss_decision"])["match_id"]
        .count()
        .reset_index(name="count")
    )

    pivot = (
        summary
        .pivot(index="year", columns="toss_decision", values="count")
        .fillna(0)
        .reset_index()
    )

    # Ensure both columns exist
    if "bat" not in pivot.columns:
        pivot["bat"] = 0
    if "field" not in pivot.columns:
        pivot["field"] = 0

    pivot["total"] = pivot["bat"] + pivot["field"]

    pivot["bat_pct"] = (pivot["bat"] / pivot["total"]) * 100
    pivot["field_pct"] = (pivot["field"] / pivot["total"]) * 100

    return pivot.sort_values("year")