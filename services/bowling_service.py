from typing import Optional

import numpy as np
import pandas as pd


def get_top_wicket_takers(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 10) -> pd.DataFrame:  # type: ignore
    """Top wicket takers with wickets by phase: PowerPlay (<6), Mid (6-15), Death (>=16)."""
    if sort_by is None:
        sort_by = "Total"
    wk = df.dropna(subset=["bowler", "player_out", "wicket_kind"]).copy()
    if wk.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    wk = wk[wk["bowler"].isin(qualified_bowlers)]
    if wk.empty:
        return pd.DataFrame()

    # Define phases
    wk["phase"] = pd.cut(
        wk["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    wk = wk[wk["phase"].notna()]

    # Total wickets
    total_wk = (
        wk.groupby("bowler", as_index=False)
        .size()
        .rename(columns={"size": "total_wickets"})
    )

    # Wickets by phase
    phase_wk = (
        wk.groupby(["bowler", "phase"], as_index=False, observed=False)
        .size()
        .pivot(index="bowler", columns="phase", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Merge
    out = total_wk.merge(phase_wk, on="bowler", how="left").fillna(0)
    out["PowerPlay"] = out["PowerPlay"].astype(int)
    out["Mid"] = out["Mid"].astype(int)
    out["Death"] = out["Death"].astype(int)

    # Sort and take top N
    sort_column = "total_wickets" if sort_by == "Total" else sort_by
    out = out.sort_values(sort_column, ascending=False).head(top_n).reset_index(drop=True)

    return out

def get_top_economy_bowlers(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 0) -> pd.DataFrame:
    """Top economy bowlers with economy by phase: PowerPlay, Mid, Death."""
    if sort_by is None:
        sort_by = "Total"
    wk = df.dropna(subset=["bowler"]).copy()
    if wk.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    wk = wk[wk["bowler"].isin(qualified_bowlers)]
    if wk.empty:
        return pd.DataFrame()

    # Define phases
    wk["phase"] = pd.cut(
        wk["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    wk = wk[wk["phase"].notna()]

    # Total economy
    total_stats = wk.groupby("bowler", as_index=False).agg(
        total_runs=("runs_batter", "sum"),
        total_balls=("valid_ball", "sum"),
    )
    total_stats["total_economy"] = total_stats.apply(
        lambda r: (r["total_runs"] / r["total_balls"] * 6) if r["total_balls"] > 0 else float("inf"),
        axis=1,
    )

    # Filter bowlers who bowled at least some balls
    total_stats = total_stats[total_stats["total_balls"] > 0]

    # Phase economies
    phase_stats = wk.groupby(["bowler", "phase"]).agg(
        {"runs_batter": "sum", "valid_ball": "sum"}
    ).reset_index().rename(columns={"runs_batter": "runs", "valid_ball": "balls"})
    phase_pivot = phase_stats.pivot(index="bowler", columns="phase", values=["runs", "balls"]).fillna(0)
    phase_pivot.columns = [f"{col[1]}_{col[0]}" for col in phase_pivot.columns]
    phase_pivot = phase_pivot.reset_index()

    # Calculate economies
    for phase in ["PowerPlay", "Mid", "Death"]:
        runs_col = f"{phase}_runs"
        balls_col = f"{phase}_balls"
        econ_col = f"{phase}_economy"
        phase_pivot[econ_col] = phase_pivot.apply(
            lambda r: (r[runs_col] / r[balls_col] * 6) if r[balls_col] > 0 else 0,
            axis=1,
        )

    # Merge
    out = total_stats.merge(phase_pivot[["bowler", "PowerPlay_economy", "Mid_economy", "Death_economy"]], on="bowler", how="left").fillna(0)

    # Sort (ascending for best economy)
    sort_column = "total_economy" if sort_by == "Total" else f"{sort_by}_economy"
    out = out.sort_values(sort_column, ascending=True).head(top_n).reset_index(drop=True)

    return out


def get_top_dot_ball_bowlers(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 0) -> pd.DataFrame:
    """Top dot ball bowlers with dot balls by phase: PowerPlay, Mid, Death."""
    if sort_by is None:
        sort_by = "Total"
    db = df.dropna(subset=["bowler"]).copy()
    if db.empty:
        return pd.DataFrame()

    # Filter for dot balls (valid balls with 0 runs)
    db = db[(db["valid_ball"] == 1) & (db["runs_batter"] == 0)]
    if db.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    db = db[db["bowler"].isin(qualified_bowlers)]
    if db.empty:
        return pd.DataFrame()

    # Define phases
    db["phase"] = pd.cut(
        db["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    db = db[db["phase"].notna()]

    # Total dot balls
    total_dots = (
        db.groupby("bowler", as_index=False)
        .size()
        .rename(columns={"size": "total_dot_balls"})
    )

    # Dot balls by phase
    phase_dots = (
        db.groupby(["bowler", "phase"], as_index=False, observed=False)
        .size()
        .pivot(index="bowler", columns="phase", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Merge
    out = total_dots.merge(phase_dots, on="bowler", how="left").fillna(0)
    out["PowerPlay"] = out["PowerPlay"].astype(int)
    out["Mid"] = out["Mid"].astype(int)
    out["Death"] = out["Death"].astype(int)

    # Sort and take top N
    sort_column = "total_dot_balls" if sort_by == "Total" else sort_by
    out = out.sort_values(sort_column, ascending=False).head(top_n).reset_index(drop=True)

    return out


def get_least_boundary_giving_bowlers(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 0) -> pd.DataFrame:
    """Least boundary giving bowlers with boundaries (4s and 6s) by phase: PowerPlay, Mid, Death."""
    if sort_by is None:
        sort_by = "Total"
    bb = df.dropna(subset=["bowler"]).copy()
    if bb.empty:
        return pd.DataFrame()

    # Filter for boundaries (4s and 6s)
    bb = bb[bb["runs_batter"].isin([4, 6])]
    if bb.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    bb = bb[bb["bowler"].isin(qualified_bowlers)]
    if bb.empty:
        return pd.DataFrame()

    # Define phases
    bb["phase"] = pd.cut(
        bb["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    bb = bb[bb["phase"].notna()]

    # Separate 4s and 6s
    bb["is_four"] = (bb["runs_batter"] == 4).astype(int)
    bb["is_six"] = (bb["runs_batter"] == 6).astype(int)

    # Total boundaries
    total_boundaries = bb.groupby("bowler", as_index=False).agg(
        total_boundaries=("runs_batter", "size"),
        total_fours=("is_four", "sum"),
        total_sixes=("is_six", "sum"),
    )

    # Boundaries by phase - get 4s and 6s for each phase
    phase_fours = bb.groupby(["bowler", "phase"])["is_four"].sum().unstack(fill_value=0).astype(int)
    phase_sixes = bb.groupby(["bowler", "phase"])["is_six"].sum().unstack(fill_value=0).astype(int)

    # Combine all data
    out = total_boundaries.copy()
    
    # Add phase columns with proper naming
    for phase in ["PowerPlay", "Mid", "Death"]:
        if phase in phase_fours.columns:
            out[f"{phase}_fours"] = out["bowler"].map(phase_fours[phase]).fillna(0).astype(int)
        else:
            out[f"{phase}_fours"] = 0
            
        if phase in phase_sixes.columns:
            out[f"{phase}_sixes"] = out["bowler"].map(phase_sixes[phase]).fillna(0).astype(int)
        else:
            out[f"{phase}_sixes"] = 0

    # Calculate phase totals for sorting
    out["PowerPlay_total"] = out["PowerPlay_fours"] + out["PowerPlay_sixes"]
    out["Mid_total"] = out["Mid_fours"] + out["Mid_sixes"]
    out["Death_total"] = out["Death_fours"] + out["Death_sixes"]

    # Sort ascending for least boundaries
    sort_column = "total_boundaries" if sort_by == "Total" else f"{sort_by}_total"
    out = out.sort_values(sort_column, ascending=True).head(top_n).reset_index(drop=True)

    # Drop phase totals as they're not needed in output
    out = out.drop(columns=["PowerPlay_total", "Mid_total", "Death_total"], errors="ignore")

    return out


def get_top_wickets_per_100_balls(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 10) -> pd.DataFrame:
    """Top wicket takers per 100 balls bowled with wickets by phase: PowerPlay (<6), Mid (6-15), Death (>=16)."""
    if sort_by is None:
        sort_by = "Total"
    wk = df.dropna(subset=["bowler", "player_out", "wicket_kind"]).copy()
    if wk.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    wk = wk[wk["bowler"].isin(qualified_bowlers)]
    if wk.empty:
        return pd.DataFrame()

    # Define phases
    wk["phase"] = pd.cut(
        wk["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    wk = wk[wk["phase"].notna()]

    # Get total balls bowled by each bowler
    total_balls = df.groupby("bowler")["valid_ball"].sum().reset_index()
    total_balls.columns = ["bowler", "total_balls"]

    # Define phases for all balls (not just wickets)
    df_copy = df.copy()
    df_copy["phase"] = pd.cut(
        df_copy["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )
    df_copy = df_copy[df_copy["phase"].notna()]

    # Get balls bowled in each phase
    phase_balls = (
        df_copy.groupby(["bowler", "phase"], as_index=False, observed=False)["valid_ball"]
        .sum()
        .pivot(index="bowler", columns="phase", values="valid_ball")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Total wickets
    total_wk = (
        wk.groupby("bowler", as_index=False)
        .size()
        .rename(columns={"size": "total_wickets"})
    )

    # Wickets by phase
    phase_wk = (
        wk.groupby(["bowler", "phase"], as_index=False, observed=False)
        .size()
        .pivot(index="bowler", columns="phase", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Merge
    out = total_wk.merge(phase_wk, on="bowler", how="left").fillna(0)
    out["PowerPlay"] = out["PowerPlay"].astype(int)
    out["Mid"] = out["Mid"].astype(int)
    out["Death"] = out["Death"].astype(int)

    # Merge with total balls
    out = out.merge(total_balls, on="bowler", how="left")

    # Merge with phase balls
    out = out.merge(phase_balls, on="bowler", how="left", suffixes=("", "_balls"))
    out["PowerPlay_balls"] = out["PowerPlay_balls"].fillna(0).astype(int)
    out["Mid_balls"] = out["Mid_balls"].fillna(0).astype(int)
    out["Death_balls"] = out["Death_balls"].fillna(0).astype(int)

    # Calculate wickets per 100 balls
    out["total_wickets_per_100"] = (out["total_wickets"] / out["total_balls"] * 100).round(2)
    out["PowerPlay_wickets_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay"] / out["PowerPlay_balls"] * 100).round(2),
        0
    )
    out["Mid_wickets_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid"] / out["Mid_balls"] * 100).round(2),
        0
    )
    out["Death_wickets_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death"] / out["Death_balls"] * 100).round(2),
        0
    )

    # Sort and take top N
    sort_column = "total_wickets_per_100" if sort_by == "Total" else f"{sort_by}_wickets_per_100"
    out = out.sort_values(sort_column, ascending=False).head(top_n).reset_index(drop=True)

    return out


def get_top_dot_balls_per_100_balls(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 0) -> pd.DataFrame:
    """Top dot ball bowlers per 100 balls bowled with dot balls by phase: PowerPlay, Mid, Death."""
    if sort_by is None:
        sort_by = "Total"
    db = df.dropna(subset=["bowler"]).copy()
    if db.empty:
        return pd.DataFrame()

    # Filter for dot balls (valid balls with 0 runs)
    db = db[(db["valid_ball"] == 1) & (db["runs_batter"] == 0)]
    if db.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    db = db[db["bowler"].isin(qualified_bowlers)]
    if db.empty:
        return pd.DataFrame()

    # Define phases
    db["phase"] = pd.cut(
        db["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    db = db[db["phase"].notna()]

    # Get total balls bowled by each bowler
    total_balls = df.groupby("bowler")["valid_ball"].sum().reset_index()
    total_balls.columns = ["bowler", "total_balls"]

    # Define phases for all balls (not just dot balls)
    df_copy = df.copy()
    df_copy["phase"] = pd.cut(
        df_copy["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )
    df_copy = df_copy[df_copy["phase"].notna()]

    # Get balls bowled in each phase
    phase_balls = (
        df_copy.groupby(["bowler", "phase"], as_index=False, observed=False)["valid_ball"]
        .sum()
        .pivot(index="bowler", columns="phase", values="valid_ball")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Total dot balls
    total_dots = (
        db.groupby("bowler", as_index=False)
        .size()
        .rename(columns={"size": "total_dot_balls"})
    )

    # Dot balls by phase
    phase_dots = (
        db.groupby(["bowler", "phase"], as_index=False, observed=False)
        .size()
        .pivot(index="bowler", columns="phase", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Merge
    out = total_dots.merge(phase_dots, on="bowler", how="left").fillna(0)
    out["PowerPlay"] = out["PowerPlay"].astype(int)
    out["Mid"] = out["Mid"].astype(int)
    out["Death"] = out["Death"].astype(int)

    # Merge with total balls
    out = out.merge(total_balls, on="bowler", how="left")

    # Merge with phase balls
    out = out.merge(phase_balls, on="bowler", how="left", suffixes=("", "_balls"))
    out["PowerPlay_balls"] = out["PowerPlay_balls"].fillna(0).astype(int)
    out["Mid_balls"] = out["Mid_balls"].fillna(0).astype(int)
    out["Death_balls"] = out["Death_balls"].fillna(0).astype(int)

    # Calculate dot balls per 100 balls
    out["total_dot_balls_per_100"] = (out["total_dot_balls"] / out["total_balls"] * 100).round(2)
    out["PowerPlay_dot_balls_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay"] / out["PowerPlay_balls"] * 100).round(2),
        0
    )
    out["Mid_dot_balls_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid"] / out["Mid_balls"] * 100).round(2),
        0
    )
    out["Death_dot_balls_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death"] / out["Death_balls"] * 100).round(2),
        0
    )

    # Sort and take top N
    sort_column = "total_dot_balls_per_100" if sort_by == "Total" else f"{sort_by}_dot_balls_per_100"
    out = out.sort_values(sort_column, ascending=False).head(top_n).reset_index(drop=True)

    return out


def get_least_boundaries_per_100_balls(df: pd.DataFrame, top_n: int = 10, sort_by: str = "Total", min_overs: int = 0) -> pd.DataFrame:
    """Least boundary giving bowlers per 100 balls bowled with boundaries (4s and 6s) by phase: PowerPlay, Mid, Death."""
    if sort_by is None:
        sort_by = "Total"
    bb = df.dropna(subset=["bowler"]).copy()
    if bb.empty:
        return pd.DataFrame()

    # Filter for boundaries (4s and 6s)
    bb = bb[bb["runs_batter"].isin([4, 6])]
    if bb.empty:
        return pd.DataFrame()

    # Filter bowlers by minimum overs bowled
    bowler_overs = df.groupby("bowler")["valid_ball"].sum() // 6
    qualified_bowlers = bowler_overs[bowler_overs >= min_overs].index
    bb = bb[bb["bowler"].isin(qualified_bowlers)]
    if bb.empty:
        return pd.DataFrame()

    # Define phases
    bb["phase"] = pd.cut(
        bb["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )

    # Filter out invalid phases (e.g., over > 20)
    bb = bb[bb["phase"].notna()]

    # Get total balls bowled by each bowler
    total_balls = df.groupby("bowler")["valid_ball"].sum().reset_index()
    total_balls.columns = ["bowler", "total_balls"]

    # Define phases for all balls (not just boundaries)
    df_copy = df.copy()
    df_copy["phase"] = pd.cut(
        df_copy["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )
    df_copy = df_copy[df_copy["phase"].notna()]

    # Get balls bowled in each phase
    phase_balls = (
        df_copy.groupby(["bowler", "phase"], as_index=False, observed=False)["valid_ball"]
        .sum()
        .pivot(index="bowler", columns="phase", values="valid_ball")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    phase_balls.columns = ["bowler", "PowerPlay_balls", "Mid_balls", "Death_balls"]

    # Boundaries by phase and type (4s and 6s)
    phase_boundaries = (
        bb.groupby(["bowler", "phase", "runs_batter"], as_index=False, observed=False)
        .size()
        .pivot(index=["bowler", "runs_batter"], columns="phase", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Melt to long format
    phase_boundaries = phase_boundaries.melt(id_vars=["bowler", "runs_batter"], value_vars=["PowerPlay", "Mid", "Death"], var_name="phase", value_name="count")

    # Pivot to wide format with bowler as index
    phase_boundaries = phase_boundaries.pivot(index="bowler", columns=["runs_batter", "phase"], values="count").fillna(0).astype(int)

    # Flatten column names
    phase_boundaries.columns = [f"{phase}_{runs}s" for runs, phase in phase_boundaries.columns]
    phase_boundaries = phase_boundaries.reset_index()

    # Total boundaries by type
    total_boundaries = (
        bb.groupby(["bowler", "runs_batter"], as_index=False)
        .size()
        .pivot(index="bowler", columns="runs_batter", values="size")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    total_boundaries.columns = ["bowler", "total_4s", "total_6s"]

    # Merge
    out = total_boundaries.merge(phase_boundaries, on="bowler", how="left").fillna(0)
    out["PowerPlay_4s"] = out["PowerPlay_4s"].astype(int)
    out["PowerPlay_6s"] = out["PowerPlay_6s"].astype(int)
    out["Mid_4s"] = out["Mid_4s"].astype(int)
    out["Mid_6s"] = out["Mid_6s"].astype(int)
    out["Death_4s"] = out["Death_4s"].astype(int)
    out["Death_6s"] = out["Death_6s"].astype(int)

    # Merge with total balls
    out = out.merge(total_balls, on="bowler", how="left")

    # Merge with phase balls
    out = out.merge(phase_balls, on="bowler", how="left")
    out["PowerPlay_balls"] = out["PowerPlay_balls"].fillna(0).astype(int)
    out["Mid_balls"] = out["Mid_balls"].fillna(0).astype(int)
    out["Death_balls"] = out["Death_balls"].fillna(0).astype(int)

    # Calculate boundaries per 100 balls
    out["total_4s_per_100"] = np.where(out["total_balls"] > 0, (out["total_4s"] / out["total_balls"] * 100).round(2), 0)
    out["total_6s_per_100"] = np.where(out["total_balls"] > 0, (out["total_6s"] / out["total_balls"] * 100).round(2), 0)
    out["total_boundaries_per_100"] = out["total_4s_per_100"] + out["total_6s_per_100"]

    out["PowerPlay_4s_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay_4s"] / out["PowerPlay_balls"] * 100).round(2),
        0
    )
    out["PowerPlay_6s_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay_6s"] / out["PowerPlay_balls"] * 100).round(2),
        0
    )
    out["PowerPlay_boundaries_per_100"] = out["PowerPlay_4s_per_100"] + out["PowerPlay_6s_per_100"]

    out["Mid_4s_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid_4s"] / out["Mid_balls"] * 100).round(2),
        0
    )
    out["Mid_6s_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid_6s"] / out["Mid_balls"] * 100).round(2),
        0
    )
    out["Mid_boundaries_per_100"] = out["Mid_4s_per_100"] + out["Mid_6s_per_100"]

    out["Death_4s_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death_4s"] / out["Death_balls"] * 100).round(2),
        0
    )
    out["Death_6s_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death_6s"] / out["Death_balls"] * 100).round(2),
        0
    )
    out["Death_boundaries_per_100"] = out["Death_4s_per_100"] + out["Death_6s_per_100"]

    # Sort ascending for least boundaries
    sort_column = "total_boundaries_per_100" if sort_by == "Total" else f"{sort_by}_boundaries_per_100"
    out = out.sort_values(sort_column, ascending=True).head(top_n).reset_index(drop=True)

    return out