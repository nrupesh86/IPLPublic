import pandas as pd

def get_titles_finals_by_team(filtered_match_df):

    finals_df = filtered_match_df[
        filtered_match_df["stage"] == "Final"
    ]

    # Final appearances
    finalists = finals_df[["year", "team_1", "team_2"]]

    finalists_long = finalists.melt(
        id_vars="year",
        value_vars=["team_1", "team_2"],
        value_name="team"
    )[["team"]]

    finals_summary = (
        finalists_long
        .groupby("team")
        .size()
        .reset_index(name="final_appearances")
    )

    # Titles
    titles_summary = (
        finals_df
        .groupby("match_won_by")
        .size()
        .reset_index(name="titles")
        .rename(columns={"match_won_by": "team"})
    )

    # Combine
    summary = finals_summary.merge(
        titles_summary,
        on="team",
        how="left"
    ).fillna(0)

    summary["titles"] = summary["titles"].astype(int)

    summary = summary.sort_values(
        "final_appearances",
        ascending=False
    )

    return summary

def get_playoff_appearances_wins_by_team(filtered_match_df):

    df = filtered_match_df.copy()

    playoff_stages = [
        "Semi Final",
        "3rd Place Play-Off",
        "Qualifier 1",
        "Qualifier 2",
        "Eliminator",
        "Elimination Final"
    ]

    playoff_df = df[
        df["stage"].isin(playoff_stages)
    ]

    # -------------------------
    # Playoff Appearances (unique per year)
    # -------------------------
    teams_df = playoff_df[["year", "team_1", "team_2"]]

    teams_long = teams_df.melt(
        id_vars="year",
        value_vars=["team_1", "team_2"],
        value_name="team"
    )[["year", "team"]]

    teams_long = teams_long.drop_duplicates(["year", "team"])

    playoff_apps = (
        teams_long
        .groupby("team")
        .size()
        .reset_index(name="playoff_appearances")
    )

    # -------------------------
    # Playoff Wins (team-year level)
    # A team gets a "win" for a year only if:
    # - it has at least one playoff win in that year, and
    # - it has zero playoff losses in that year
    # -------------------------
    playoff_teams = playoff_df[["year", "date", "team_1", "team_2", "match_won_by"]]

    team1_rows = playoff_teams.rename(columns={"team_1": "team"})[
        ["year", "date", "team", "match_won_by"]
    ]
    team2_rows = playoff_teams.rename(columns={"team_2": "team"})[
        ["year", "date", "team", "match_won_by"]
    ]

    playoff_long = pd.concat([team1_rows, team2_rows], ignore_index=True)
    playoff_long["is_win"] = playoff_long["team"] == playoff_long["match_won_by"]
    playoff_long["is_loss"] = (
        playoff_long["match_won_by"].notna()
        & (playoff_long["team"] != playoff_long["match_won_by"])
    )
    playoff_long["win_date"] = playoff_long["date"].where(playoff_long["is_win"])
    playoff_long["loss_date"] = playoff_long["date"].where(playoff_long["is_loss"])

    year_team_outcome = (
        playoff_long
        .groupby(["year", "team"], as_index=False)
        .agg(
            wins=("is_win", "sum"),
            losses=("is_loss", "sum"),
            latest_win_date=("win_date", "max"),
            latest_loss_date=("loss_date", "max"),
        )
    )

    year_team_outcome["year_win"] = (
        (year_team_outcome["wins"] > 0)
        & (
            (year_team_outcome["losses"] == 0)
            | (year_team_outcome["latest_win_date"] > year_team_outcome["latest_loss_date"])
        )
    ).astype(int)

    playoff_wins = (
        year_team_outcome
        .groupby("team", as_index=False)["year_win"]
        .sum()
        .rename(columns={"year_win": "playoff_wins"})
    )

    # -------------------------
    # Combine
    # -------------------------
    summary = playoff_apps.merge(
        playoff_wins,
        on="team",
        how="left"
    ).fillna(0)

    summary["playoff_wins"] = summary["playoff_wins"].astype(int)

    return summary.sort_values("playoff_appearances", ascending=False)

def get_head_to_head_win(filtered_match_df):

    df = filtered_match_df.copy()
    df = df[df["match_won_by"].notna()]

    team1_df = df[["team_1", "team_2", "match_won_by"]].rename(
        columns={"team_1": "team", "team_2": "opponent"}
    )

    team2_df = df[["team_1", "team_2", "match_won_by"]].rename(
        columns={"team_2": "team", "team_1": "opponent"}
    )

    combined = pd.concat([team1_df, team2_df])

    combined["win"] = combined["team"] == combined["match_won_by"]

    summary = (
        combined
        .groupby(["team", "opponent"])
        .agg(
            matches=("win", "count"),
            wins=("win", "sum")
        )
        .reset_index()
    )

    summary["win_pct"] = summary["wins"] / summary["matches"] * 100

    # Pivot all 3 matrices
    win_pct_matrix = summary.pivot(
        index="team", columns="opponent", values="win_pct"
    )

    wins_matrix = summary.pivot(
        index="team", columns="opponent", values="wins"
    )

    matches_matrix = summary.pivot(
        index="team", columns="opponent", values="matches"
    )

    return (
        win_pct_matrix.round(1),
        wins_matrix,
        matches_matrix
    )

def get_team_win_pct(filtered_match_df):

    df = filtered_match_df.copy()

    # keep only valid matches
    df = df[df["match_won_by"].notna()]

    team1_df = df[["team_1", "match_won_by"]].rename(
        columns={"team_1": "team"}
    )

    team2_df = df[["team_2", "match_won_by"]].rename(
        columns={"team_2": "team"}
    )

    combined = pd.concat([team1_df, team2_df])

    combined["win"] = combined["team"] == combined["match_won_by"]

    summary = (
        combined
        .groupby("team")
        .agg(
            matches=("win", "count"),
            wins=("win", "sum")
        )
        .reset_index()
    )

    summary["win_pct"] = summary["wins"] / summary["matches"] * 100

    return summary.sort_values("win_pct", ascending=False)

def get_team_win_pct_by_season(filtered_match_df):

    df = filtered_match_df.copy()
    df = df[df["match_won_by"].notna()]

    # create long format
    team1_df = df[["year", "team_1", "match_won_by"]].rename(
        columns={"team_1": "team"}
    )

    team2_df = df[["year", "team_2", "match_won_by"]].rename(
        columns={"team_2": "team"}
    )

    combined = pd.concat([team1_df, team2_df])

    combined["win"] = combined["team"] == combined["match_won_by"]

    summary = (
        combined
        .groupby(["year", "team"])
        .agg(
            matches=("win", "count"),
            wins=("win", "sum")
        )
        .reset_index()
    )

    summary["win_pct"] = summary["wins"] / summary["matches"] * 100

    return summary