import streamlit as st

def season_filter(
        df,
        label="Select Season(s)",
        key="season_filter",
        location="main" # "main" or "sidebar"
    ):
    """
    Reusable season multiselect filter.
    Returns selected years.
    """

    available_years = sorted(df["year"].unique())

    container = st.sidebar if location == "sidebar" else st

    selected_years = container.multiselect(
        label,
        available_years,
        default=available_years,
        key=key
    )

    return selected_years