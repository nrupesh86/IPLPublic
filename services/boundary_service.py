import pandas as pd

def get_boundaries_per_season(df: pd.DataFrame, match_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns totals and per-match averages of 4s and 6s per season.
    """

    # Filter boundaries
    boundaries = df[df["runs_batter"].isin([4, 6])]

    totals = (
        boundaries
        .groupby(["year", "runs_batter"])
        .size()
        .reset_index(name="count")
        .pivot(index="year", columns="runs_batter", values="count")
        .fillna(0)
        .reset_index()
    )

    totals = totals.rename(columns={4: "fours", 6: "sixes"})

    # Match counts per season
    matches_per_season = (
        match_df
        .groupby("year")["match_id"]
        .nunique()
        .reset_index(name="matches")
    )

    # Merge
    merged = totals.merge(matches_per_season, on="year", how="left")

    # Compute averages
    merged["avg_fours"] = merged["fours"] / merged["matches"]
    merged["avg_sixes"] = merged["sixes"] / merged["matches"]

    return merged.sort_values("year")