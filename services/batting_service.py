from typing import cast
import pandas as pd

def get_dismissal_type_rankings(
    df: pd.DataFrame,
    min_runs: int,
    top_n: int,
    top_k_types: int = 6,
) -> pd.DataFrame:
    """
    Returns a long dataframe for a clustered chart of dismissal types.

    - Dismissals are counted from ball-level rows where (player_out, wicket_kind) are present.
    - Eligible batters: total_runs >= min_runs and at least 1 dismissal.
    - Top N batters are chosen by total runs (descending).
    - Dismissal types are grouped to the top K types (overall in selection) + "Other".
    """
    bat = df.dropna(subset=["batter"]).copy()
    runs = bat.groupby("batter", as_index=False)["runs_batter"].sum()
    runs = runs.rename(columns={"batter": "player", "runs_batter": "total_runs"})  # type: ignore

    outs = df.dropna(subset=["player_out", "wicket_kind"]).copy()
    dismissal_long = (
        outs.groupby(["player_out", "wicket_kind"])
        .size()
        .to_frame("dismissals")
        .reset_index()
    )
    dismissal_long.columns = ["player", "wicket_kind", "dismissals"]

    merged = dismissal_long.merge(runs, on="player", how="left")
    merged["total_runs"] = merged["total_runs"].fillna(0)
    merged = merged[merged["total_runs"] >= min_runs]

    totals = (
        merged.groupby("player", as_index=False)
        .agg(
            total_dismissals=("dismissals", "sum"),
            total_runs=("total_runs", "max"),
        )
    )
    merged = merged.merge(
        totals[["player", "total_dismissals"]],
        on="player",
        how="left",
    )

    # keep only players with at least one dismissal
    merged = merged[merged["total_dismissals"] > 0]

    top_players = (
        totals[totals["total_dismissals"] > 0]
        .sort_values("total_runs", ascending=False)
        .head(top_n)["player"]
        .tolist()
    )
    merged = merged[merged["player"].isin(top_players)]

    # pick top K dismissal types in this selection
    top_types = (
        merged.groupby("wicket_kind", as_index=False)["dismissals"]
        .sum()
        .sort_values(by="dismissals", ascending=False)  # type: ignore
        .head(top_k_types)["wicket_kind"]
        .tolist()
    )

    merged["wicket_kind_group"] = merged["wicket_kind"].where(
        merged["wicket_kind"].isin(top_types), "Other"
    )

    final_long = (
        merged.groupby(["player", "wicket_kind_group"], as_index=False)
        .agg(
            dismissals=("dismissals", "sum"),
            total_runs=("total_runs", "max"),
            total_dismissals=("total_dismissals", "max"),
        )
    )

    # keep player ordering by total runs (desc)
    order = (
        final_long.groupby("player", as_index=False)["total_runs"]
        .max()
        .sort_values(by="total_runs", ascending=False)  # type: ignore
        ["player"]
        .tolist()
    )
    final_long["player"] = pd.Categorical(final_long["player"], categories=order, ordered=True)
    final_long = final_long.sort_values(["player", "dismissals"], ascending=[True, False])

    return final_long

def get_batting_average_rankings(
    df: pd.DataFrame,
    min_runs: int,
    sort_by: str = "strike_rate",
) -> pd.DataFrame:
    """
    Batting average = total runs / dismissals, where dismissals are rows with
    a wicket and player_out equal to the batter's name.
    Strike rate = (total runs / balls faced) * 100, with balls faced = legal
    deliveries (valid_ball == 1) where the player was the striker.
    Eligible players must have total_runs >= min_runs and at least one dismissal.
    sort_by: "average" or "strike_rate" (default).
    """
    bat = df.dropna(subset=["batter"]).copy()

    runs = bat.groupby("batter", as_index=False)["runs_batter"].sum()
    runs = runs.rename(columns={"batter": "player", "runs_batter": "total_runs"})  # type: ignore

    legal = bat[bat["valid_ball"] == 1]
    balls = legal.groupby("batter").size().to_frame("balls_faced").reset_index()
    balls.columns = ["player", "balls_faced"]

    wk = df.dropna(subset=["player_out", "wicket_kind"]).copy()
    dismissals = wk.groupby("player_out").size().to_frame("dismissals").reset_index()
    dismissals.columns = ["player", "dismissals"]

    merged = runs.merge(balls, on="player", how="left")
    merged["balls_faced"] = merged["balls_faced"].fillna(0).astype(int)
    merged = merged.merge(dismissals, on="player", how="left")
    merged["dismissals"] = merged["dismissals"].fillna(0).astype(int)
    merged = merged[merged["dismissals"] > 0].copy()
    merged["average"] = merged["total_runs"] / merged["dismissals"]
    merged["strike_rate"] = merged["total_runs"] / merged["balls_faced"] * 100
    merged = merged[merged["balls_faced"] > 0]
    merged = merged[merged["total_runs"] >= min_runs]
    merged_df = cast(pd.DataFrame, merged)

    if sort_by == "strike_rate":
        return merged_df.sort_values(by="strike_rate", ascending=False).reset_index(drop=True)
    return merged_df.sort_values(by="average", ascending=False).reset_index(drop=True)


def get_boundary_rankings(
    df: pd.DataFrame,
    min_runs: int,
    sort_by: str = "sixes",
) -> pd.DataFrame:
    """
    Per-batter counts of 4s and 6s (runs_batter), plus combined (4s + 6s).
    Eligible players must have total_runs >= min_runs.
    sort_by: "sixes" (default), "fours", or "combined".
    """
    bat = df.dropna(subset=["batter"]).copy()
    runs = bat.groupby("batter", as_index=False)["runs_batter"].sum()
    runs = runs.rename(columns={"batter": "player", "runs_batter": "total_runs"})  # type: ignore

    br = bat["runs_batter"]
    fours = (
        bat[br == 4]
        .groupby("batter")
        .size()
        .to_frame("fours")
        .reset_index()
    )
    fours.columns = ["player", "fours"]
    sixes = (
        bat[br == 6]
        .groupby("batter")
        .size()
        .to_frame("sixes")
        .reset_index()
    )
    sixes.columns = ["player", "sixes"]

    merged = runs.merge(fours, on="player", how="left").merge(sixes, on="player", how="left")
    merged["fours"] = merged["fours"].fillna(0).astype(int)
    merged["sixes"] = merged["sixes"].fillna(0).astype(int)
    merged["combined"] = merged["fours"] + merged["sixes"]
    merged = merged[merged["total_runs"] >= min_runs]
    merged_df = cast(pd.DataFrame, merged)

    if sort_by == "fours":
        return merged_df.sort_values(by="fours", ascending=False).reset_index(drop=True)
    if sort_by == "combined":
        return merged_df.sort_values(by="combined", ascending=False).reset_index(drop=True)
    return merged_df.sort_values(by="sixes", ascending=False).reset_index(drop=True)


def get_top_run_scorers(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Top run scorers with batting run split by:
    - boundaries vs non-boundaries
    - powerplay vs non-powerplay
    """
    bat = df.dropna(subset=["batter"]).copy()
    bat["is_four"] = bat["runs_batter"].eq(4).astype(int)
    bat["is_six"] = bat["runs_batter"].eq(6).astype(int)
    bat["powerplay_component"] = bat["runs_batter"].where(bat["over"] < 6, 0)

    grouped = (
        bat.groupby("batter")
        .agg(
            total_runs=("runs_batter", "sum"),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            powerplay_runs=("powerplay_component", "sum"),
        )
        .reset_index()
        .rename(columns={"batter": "player"})
    )
    grouped["boundary_runs"] = grouped["fours"] * 4 + grouped["sixes"] * 6
    grouped["non_boundary_runs"] = grouped["total_runs"] - grouped["boundary_runs"]
    grouped["non_powerplay_runs"] = grouped["total_runs"] - grouped["powerplay_runs"]

    grouped = grouped.sort_values("total_runs", ascending=False).head(top_n)
    return grouped
