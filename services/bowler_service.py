from typing import Optional

import numpy as np
import pandas as pd


def _add_phase(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["phase"] = pd.cut(
        df["over"],
        bins=[-1, 5, 15, float("inf")],
        labels=["PowerPlay", "Mid", "Death"],
    )
    return df[df["phase"].notna()]


def get_career_wickets_leader(df: pd.DataFrame) -> Optional[str]:
    wk = df.dropna(subset=["bowler", "player_out", "wicket_kind"]).copy()
    if wk.empty:
        return None
    totals = wk.groupby("bowler").size()
    if totals.empty:
        return None
    return str(totals.idxmax())


def _ensure_phase_columns(out: pd.DataFrame, cols):
    for c in cols:
        if c not in out.columns:
            out[c] = 0
    return out


def get_bowler_wickets_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.dropna(subset=["bowler", "player_out", "wicket_kind"]).copy()
    if pdf.empty:
        return pd.DataFrame()

    pdf = _add_phase(pdf)
    wk = (
        pdf.groupby(["year", "phase"], as_index=False)
        .size()
        .pivot(index="year", columns="phase", values="size")
        .fillna(0)
        .reset_index()
    )
    wk = _ensure_phase_columns(wk, ["PowerPlay", "Mid", "Death"])
    wk["total_wickets"] = wk[["PowerPlay", "Mid", "Death"]].sum(axis=1)
    return wk.sort_values("year").reset_index(drop=True)


def get_bowler_wickets_per_100_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    base = pdf.dropna(subset=["bowler"]).copy()
    if base.empty:
        return pd.DataFrame()

    wk = base.dropna(subset=["player_out", "wicket_kind"]).copy()
    if wk.empty:
        return pd.DataFrame()

    wk = _add_phase(wk)
    if wk.empty:
        return pd.DataFrame()

    # Total balls by season (same baseline as bowling analytics Top-N logic)
    total_balls = base.groupby("year")["valid_ball"].sum().rename("total_balls")

    # Phase balls by season from phased deliveries
    phased_base = _add_phase(base)
    phase_balls = (
        phased_base.groupby(["year", "phase"], observed=False)["valid_ball"]
        .sum()
        .unstack(fill_value=0)
    )

    # Wickets by season and phase
    total_wk = wk.groupby("year").size().rename("total_wickets")
    phase_wk = (
        wk.groupby(["year", "phase"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    phase_cols = ["PowerPlay", "Mid", "Death"]
    phase_balls = phase_balls.reindex(columns=phase_cols, fill_value=0)
    phase_wk = phase_wk.reindex(columns=phase_cols, fill_value=0)

    # Build a complete year index from all ingredients
    years = sorted(set(total_balls.index) | set(total_wk.index) | set(phase_balls.index) | set(phase_wk.index))
    out = pd.DataFrame({"year": years})

    out = out.merge(total_balls.reset_index(), on="year", how="left")
    out = out.merge(total_wk.reset_index(), on="year", how="left")
    out = out.merge(phase_balls.reset_index(), on="year", how="left", suffixes=("", "_balls"))
    out = out.merge(phase_wk.reset_index(), on="year", how="left", suffixes=("_balls", ""))

    out["total_balls"] = out["total_balls"].fillna(0)
    out["total_wickets"] = out["total_wickets"].fillna(0)

    for col in phase_cols:
        balls_col = f"{col}_balls"
        wickets_col = col
        if balls_col not in out.columns:
            out[balls_col] = 0
        if wickets_col not in out.columns:
            out[wickets_col] = 0

        out[balls_col] = out[balls_col].fillna(0)
        out[wickets_col] = out[wickets_col].fillna(0)

    out["total_wickets_per_100"] = np.where(
        out["total_balls"] > 0,
        (out["total_wickets"] / out["total_balls"] * 100).round(2),
        0,
    )
    out["PowerPlay_wickets_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay"] / out["PowerPlay_balls"] * 100).round(2),
        0,
    )
    out["Mid_wickets_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid"] / out["Mid_balls"] * 100).round(2),
        0,
    )
    out["Death_wickets_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death"] / out["Death_balls"] * 100).round(2),
        0,
    )

    # Preserve raw wicket counts for tooltip usage.
    out["PowerPlay_wickets"] = out["PowerPlay"]
    out["Mid_wickets"] = out["Mid"]
    out["Death_wickets"] = out["Death"]

    # Backward-compatible aliases used elsewhere in this tab.
    out["PowerPlay"] = out["PowerPlay_wickets_per_100"]
    out["Mid"] = out["Mid_wickets_per_100"]
    out["Death"] = out["Death_wickets_per_100"]

    return out.fillna(0).round(2).sort_values("year").reset_index(drop=True)


def get_bowler_economy_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    base = pdf.dropna(subset=["bowler"]).copy()
    if base.empty:
        return pd.DataFrame()

    phased = _add_phase(base)
    if phased.empty:
        return pd.DataFrame()

    total_stats = base.groupby("year", as_index=False).agg(
        total_runs=("runs_batter", "sum"),
        total_balls=("valid_ball", "sum"),
    )
    total_stats["total_economy"] = np.where(
        total_stats["total_balls"] > 0,
        total_stats["total_runs"] / total_stats["total_balls"] * 6,
        0,
    )

    phase_stats = (
        phased.groupby(["year", "phase"], observed=False)[["runs_batter", "valid_ball"]]
        .sum()
        .reset_index()
        .rename(columns={"runs_batter": "runs", "valid_ball": "balls"})
    )
    phase_pivot = phase_stats.pivot(index="year", columns="phase", values=["runs", "balls"]).fillna(0)
    phase_pivot.columns = [f"{col[1]}_{col[0]}" for col in phase_pivot.columns]
    phase_pivot = phase_pivot.reset_index()

    for phase in ["PowerPlay", "Mid", "Death"]:
        runs_col = f"{phase}_runs"
        balls_col = f"{phase}_balls"
        if runs_col not in phase_pivot.columns:
            phase_pivot[runs_col] = 0
        if balls_col not in phase_pivot.columns:
            phase_pivot[balls_col] = 0

    out = total_stats.merge(phase_pivot, on="year", how="left").fillna(0)

    for phase in ["PowerPlay", "Mid", "Death"]:
        runs_col = f"{phase}_runs"
        balls_col = f"{phase}_balls"
        econ_col = f"{phase}_economy"
        out[econ_col] = np.where(
            out[balls_col] > 0,
            out[runs_col] / out[balls_col] * 6,
            0,
        )

    # Backward-compatible aliases used by existing chart code in this tab.
    out["PowerPlay"] = out["PowerPlay_economy"]
    out["Mid"] = out["Mid_economy"]
    out["Death"] = out["Death_economy"]

    return out.round(2).sort_values("year").reset_index(drop=True)


def get_bowler_dot_balls_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    base = pdf.dropna(subset=["bowler"]).copy()
    if base.empty:
        return pd.DataFrame()

    phased = _add_phase(base)
    if phased.empty:
        return pd.DataFrame()

    # Dot balls are legal deliveries with zero runs off the bat.
    dots = phased[(phased["valid_ball"] == 1) & (phased["runs_batter"] == 0)]

    phase_dots = (
        dots.groupby(["year", "phase"], as_index=False, observed=False)
        .size()
        .pivot(index="year", columns="phase", values="size")
        .fillna(0)
        .reset_index()
    )
    phase_dots = _ensure_phase_columns(phase_dots, ["PowerPlay", "Mid", "Death"])

    # Keep all seasons present for this bowler even when no dot ball in a phase/year.
    years_df = pd.DataFrame({"year": sorted(phased["year"].dropna().unique())})
    out = years_df.merge(phase_dots, on="year", how="left").fillna(0)

    out["PowerPlay"] = out["PowerPlay"].astype(int)
    out["Mid"] = out["Mid"].astype(int)
    out["Death"] = out["Death"].astype(int)
    out["total_dot_balls"] = out[["PowerPlay", "Mid", "Death"]].sum(axis=1).astype(int)
    return out.sort_values("year").reset_index(drop=True)


def get_bowler_dot_balls_per_100_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    base = pdf.dropna(subset=["bowler"]).copy()
    if base.empty:
        return pd.DataFrame()

    phased = _add_phase(base)
    if phased.empty:
        return pd.DataFrame()

    dots = phased[(phased["valid_ball"] == 1) & (phased["runs_batter"] == 0)]

    total_balls = base.groupby("year")["valid_ball"].sum().rename("total_balls")
    total_dots = dots.groupby("year").size().rename("total_dot_balls")

    phase_balls = (
        phased.groupby(["year", "phase"], observed=False)["valid_ball"]
        .sum()
        .unstack(fill_value=0)
    )
    phase_dots = (
        dots.groupby(["year", "phase"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    phase_cols = ["PowerPlay", "Mid", "Death"]
    phase_balls = phase_balls.reindex(columns=phase_cols, fill_value=0)
    phase_dots = phase_dots.reindex(columns=phase_cols, fill_value=0)

    years = sorted(set(total_balls.index) | set(total_dots.index) | set(phase_balls.index) | set(phase_dots.index))
    out = pd.DataFrame({"year": years})

    out = out.merge(total_balls.reset_index(), on="year", how="left")
    out = out.merge(total_dots.reset_index(), on="year", how="left")
    out = out.merge(phase_balls.reset_index(), on="year", how="left", suffixes=("", "_balls"))
    out = out.merge(phase_dots.reset_index(), on="year", how="left", suffixes=("_balls", ""))

    out["total_balls"] = out["total_balls"].fillna(0)
    out["total_dot_balls"] = out["total_dot_balls"].fillna(0)

    for col in phase_cols:
        balls_col = f"{col}_balls"
        dots_col = col
        if balls_col not in out.columns:
            out[balls_col] = 0
        if dots_col not in out.columns:
            out[dots_col] = 0

        out[balls_col] = out[balls_col].fillna(0)
        out[dots_col] = out[dots_col].fillna(0)

    out["total_dot_balls_per_100"] = np.where(
        out["total_balls"] > 0,
        (out["total_dot_balls"] / out["total_balls"] * 100).round(2),
        0,
    )
    out["PowerPlay_dot_balls_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay"] / out["PowerPlay_balls"] * 100).round(2),
        0,
    )
    out["Mid_dot_balls_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid"] / out["Mid_balls"] * 100).round(2),
        0,
    )
    out["Death_dot_balls_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death"] / out["Death_balls"] * 100).round(2),
        0,
    )

    # Preserve raw dot-ball counts for tooltip usage.
    out["PowerPlay_dot_balls"] = out["PowerPlay"]
    out["Mid_dot_balls"] = out["Mid"]
    out["Death_dot_balls"] = out["Death"]

    # Backward-compatible aliases for existing chart references.
    out["PowerPlay"] = out["PowerPlay_dot_balls_per_100"]
    out["Mid"] = out["Mid_dot_balls_per_100"]
    out["Death"] = out["Death_dot_balls_per_100"]

    return out.fillna(0).round(2).sort_values("year").reset_index(drop=True)


def get_bowler_boundaries_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.dropna(subset=["bowler"]).copy()
    if pdf.empty:
        return pd.DataFrame()

    pdf = _add_phase(pdf)
    boundaries = pdf[pdf["runs_batter"].isin([4, 6])]

    phase_bnd = (
        boundaries.groupby(["year", "phase"], as_index=False).size()
        .pivot(index="year", columns="phase", values="size")
        .fillna(0)
        .reset_index()
    )
    phase_bnd = _ensure_phase_columns(phase_bnd, ["PowerPlay", "Mid", "Death"])
    phase_bnd["total_boundaries"] = phase_bnd[["PowerPlay", "Mid", "Death"]].sum(axis=1)
    return phase_bnd.sort_values("year").reset_index(drop=True)


def get_bowler_boundaries_per_100_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    base = pdf.dropna(subset=["bowler"]).copy()
    if base.empty:
        return pd.DataFrame()

    phased = _add_phase(base)
    if phased.empty:
        return pd.DataFrame()

    boundaries = phased[phased["runs_batter"].isin([4, 6])]

    total_balls = base.groupby("year")["valid_ball"].sum().rename("total_balls")
    total_boundaries = boundaries.groupby("year").size().rename("total_boundaries")

    phase_balls = (
        phased.groupby(["year", "phase"], observed=False)["valid_ball"]
        .sum()
        .unstack(fill_value=0)
    )
    phase_boundaries = (
        boundaries.groupby(["year", "phase"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    phase_cols = ["PowerPlay", "Mid", "Death"]
    phase_balls = phase_balls.reindex(columns=phase_cols, fill_value=0)
    phase_boundaries = phase_boundaries.reindex(columns=phase_cols, fill_value=0)

    years = sorted(set(total_balls.index) | set(total_boundaries.index) | set(phase_balls.index) | set(phase_boundaries.index))
    out = pd.DataFrame({"year": years})

    out = out.merge(total_balls.reset_index(), on="year", how="left")
    out = out.merge(total_boundaries.reset_index(), on="year", how="left")
    out = out.merge(phase_balls.reset_index(), on="year", how="left", suffixes=("", "_balls"))
    out = out.merge(phase_boundaries.reset_index(), on="year", how="left", suffixes=("_balls", ""))

    out["total_balls"] = out["total_balls"].fillna(0)
    out["total_boundaries"] = out["total_boundaries"].fillna(0)

    for col in phase_cols:
        balls_col = f"{col}_balls"
        boundaries_col = col
        if balls_col not in out.columns:
            out[balls_col] = 0
        if boundaries_col not in out.columns:
            out[boundaries_col] = 0

        out[balls_col] = out[balls_col].fillna(0)
        out[boundaries_col] = out[boundaries_col].fillna(0)

    out["total_boundaries_per_100"] = np.where(
        out["total_balls"] > 0,
        (out["total_boundaries"] / out["total_balls"] * 100).round(2),
        0,
    )
    out["PowerPlay_boundaries_per_100"] = np.where(
        out["PowerPlay_balls"] > 0,
        (out["PowerPlay"] / out["PowerPlay_balls"] * 100).round(2),
        0,
    )
    out["Mid_boundaries_per_100"] = np.where(
        out["Mid_balls"] > 0,
        (out["Mid"] / out["Mid_balls"] * 100).round(2),
        0,
    )
    out["Death_boundaries_per_100"] = np.where(
        out["Death_balls"] > 0,
        (out["Death"] / out["Death_balls"] * 100).round(2),
        0,
    )

    # Preserve raw boundary counts for tooltip usage.
    out["PowerPlay_boundaries"] = out["PowerPlay"]
    out["Mid_boundaries"] = out["Mid"]
    out["Death_boundaries"] = out["Death"]

    # Backward-compatible aliases for existing chart references.
    out["PowerPlay"] = out["PowerPlay_boundaries_per_100"]
    out["Mid"] = out["Mid_boundaries_per_100"]
    out["Death"] = out["Death_boundaries_per_100"]

    return out.fillna(0).round(2).sort_values("year").reset_index(drop=True)
