from typing import Optional

import pandas as pd


def get_career_runs_leader(df: pd.DataFrame) -> Optional[str]:
    """Batter with highest career runs (sum of runs_batter) in the full dataset."""
    bat = df.dropna(subset=["batter"])
    if bat.empty:
        return None
    totals = bat.groupby("batter")["runs_batter"].sum()
    return str(totals.idxmax())


def get_player_runs_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    """Per-year runs split: boundary / non-boundary / powerplay / non-powerplay."""
    pdf = pdf.dropna(subset=["batter"]).copy()
    if pdf.empty:
        return pd.DataFrame()

    pdf["is_four"] = pdf["runs_batter"].eq(4).astype(int)
    pdf["is_six"] = pdf["runs_batter"].eq(6).astype(int)
    pdf["powerplay_component"] = pdf["runs_batter"].where(pdf["over"] < 6, 0)

    g = (
        pdf.groupby("year", as_index=False)
        .agg(
            total_runs=("runs_batter", "sum"),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            powerplay_runs=("powerplay_component", "sum"),
        )
        .sort_values("year")
    )
    g["boundary_runs"] = g["fours"] * 4 + g["sixes"] * 6
    g["non_boundary_runs"] = g["total_runs"] - g["boundary_runs"]
    g["non_powerplay_runs"] = g["total_runs"] - g["powerplay_runs"]
    return g.reset_index(drop=True)


def get_player_avg_sr_by_year(tab_df: pd.DataFrame, pdf: pd.DataFrame) -> pd.DataFrame:
    """Per-year average and strike rate for one batter (pdf = their ball rows in tab scope)."""
    pdf = pdf.dropna(subset=["batter"]).copy()
    if pdf.empty:
        return pd.DataFrame()

    batter = pdf["batter"].iloc[0]
    runs_y = pdf.groupby("year", as_index=False)["runs_batter"].sum()
    runs_y = runs_y.rename(columns={"runs_batter": "total_runs"})  # type: ignore

    legal = pdf[pdf["valid_ball"] == 1]
    balls_y = legal.groupby("year").size().reset_index(name="balls_faced")

    wk = tab_df.dropna(subset=["player_out", "wicket_kind"]).copy()
    wk = wk[wk["player_out"] == batter]
    dis_y = wk.groupby("year").size().reset_index(name="dismissals")

    out = runs_y.merge(balls_y, on="year", how="left").merge(dis_y, on="year", how="left")
    out["balls_faced"] = out["balls_faced"].fillna(0).astype(int)
    out["dismissals"] = out["dismissals"].fillna(0).astype(int)

    out["average"] = out.apply(
        lambda r: r["total_runs"] / r["dismissals"] if r["dismissals"] > 0 else float("nan"),
        axis=1,
    )
    out["strike_rate"] = out.apply(
        lambda r: (r["total_runs"] / r["balls_faced"] * 100) if r["balls_faced"] > 0 else float("nan"),
        axis=1,
    )
    return out.sort_values("year").reset_index(drop=True)


def get_player_boundaries_by_year(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.dropna(subset=["batter"]).copy()
    if pdf.empty:
        return pd.DataFrame()

    br = pdf["runs_batter"]
    fours = (
        pdf[br == 4].groupby("year").size().to_frame("fours").reset_index()
    )
    sixes = (
        pdf[br == 6].groupby("year").size().to_frame("sixes").reset_index()
    )
    years = pd.DataFrame({"year": sorted(pdf["year"].dropna().unique())})
    out = years.merge(fours, on="year", how="left").merge(sixes, on="year", how="left")
    out["fours"] = out["fours"].fillna(0).astype(int)
    out["sixes"] = out["sixes"].fillna(0).astype(int)
    out["combined"] = out["fours"] + out["sixes"]
    return out.sort_values("year").reset_index(drop=True)


def get_player_dismissals_by_year(
    df: pd.DataFrame,
    batter_name: Optional[str],
    top_k_types: int = 8,
) -> pd.DataFrame:
    """Long-format: year, wicket_kind_group, dismissals for stacked chart."""
    if batter_name is None:
        return pd.DataFrame()
    wk = df.dropna(subset=["player_out", "wicket_kind"]).copy()
    wk = wk[wk["player_out"] == batter_name]
    if wk.empty:
        return pd.DataFrame()

    cnt = (
        wk.groupby(["year", "wicket_kind"])
        .size()
        .reset_index(name="dismissals")
    )

    top_types = (
        cnt.groupby("wicket_kind", as_index=False)["dismissals"]
        .sum()
        .sort_values(by="dismissals", ascending=False)  # type: ignore
        .head(top_k_types)["wicket_kind"]
        .tolist()
    )
    cnt["wicket_kind_group"] = cnt["wicket_kind"].where(
        cnt["wicket_kind"].isin(top_types), "Other"
    )

    out = (
        cnt.groupby(["year", "wicket_kind_group"], as_index=False)["dismissals"]
        .sum()
        .sort_values(by=["year", "dismissals"], ascending=[True, False])  # type: ignore
    )
    return out.reset_index(drop=True)
