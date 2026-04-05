from pathlib import Path

import pandas as pd
import streamlit as st
from utils.venue_mapping import venue_mapping
from utils.team_mapping import team_mapping
from utils.venue_city_mapping import venue_city_mapping

@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[1]
    preferred = project_root / "data" / "IPL.csv"
    fallback = project_root / "data" / "ipl.csv"

    csv_path = preferred if preferred.exists() else fallback
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at {preferred} or {fallback}")

    df = pd.read_csv(csv_path, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    # Clean venue names
    df["venue"] = (
        df["venue"]
        .str.strip()
        .replace(venue_mapping)
    )

    # Clean team names
    df["batting_team"] = (
        df["batting_team"]
        .str.strip()
        .replace(team_mapping)
    )

    df["bowling_team"] = (
        df["bowling_team"]
        .str.strip()
        .replace(team_mapping)
    )

    df["match_won_by"] = (
        df["match_won_by"]
        .str.strip()
        .replace(team_mapping)
    )

    # Clean up certain city values based on venue - city mapping
    df["city"] = df.apply(
        lambda row: venue_city_mapping.get(row["venue"], row["city"]),
        axis=1
    )

    df = df.rename(columns={
        "runs_not_boundary": "runs_boundary"
    })

    return df