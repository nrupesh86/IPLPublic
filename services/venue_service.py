import pandas as pd

def get_team_results_by_venue(filtered_match_df, top_n):

    top_venues = (
        filtered_match_df
        .groupby("venue")["match_id"]
        .count()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    df = filtered_match_df[filtered_match_df["venue"].isin(top_venues)].copy()

    # create winner/loser rows
    winners = df[["venue", "match_won_by"]].rename(
        columns={"match_won_by": "team"}
    )
    winners["result"] = "Win"

    losers = df.copy()
    losers["team"] = losers.apply(
        lambda r: r["team_1"] if r["match_won_by"] == r["team_2"] else r["team_2"],
        axis=1
    )
    losers = losers[["venue", "team"]]
    losers["result"] = "Loss"

    combined = pd.concat([winners, losers])

    summary = (
        combined
        .groupby(["venue", "team", "result"])
        .size()
        .reset_index(name="count")
    )

    return summary

def get_innings_results_by_venue(filtered_match_df, top_n):

    df = filtered_match_df.copy()

    # Identify batting-first team
    df["bat_first_team"] = df["team_1"]

    # Check if batting-first team won
    df["bat_first_win"] = df["match_won_by"] == df["bat_first_team"]

    venue_summary = (
        df.groupby("venue")
        .agg(
            matches=("match_id", "count"),
            bat_first_wins=("bat_first_win", "sum")
        )
        .reset_index()
    )

    venue_summary["bowl_first_wins"] = (
        venue_summary["matches"] - venue_summary["bat_first_wins"]
    )

    venue_summary["bat_first_pct"] = (
        venue_summary["bat_first_wins"] / venue_summary["matches"] * 100
    )

    venue_summary["bowl_first_pct"] = (
        venue_summary["bowl_first_wins"] / venue_summary["matches"] * 100
    )

    # select top venues
    top_venues = (
        venue_summary
        .sort_values("matches", ascending=False)
        .head(top_n)["venue"]
    )

    venue_summary = venue_summary[
        venue_summary["venue"].isin(top_venues)
    ]

    return venue_summary.sort_values("matches", ascending=False)

def get_toss_impact_by_venue(filtered_match_df, top_n):

    df = filtered_match_df.copy()

    df["toss_match_win"] = df["toss_winner"] == df["match_won_by"]

    venue_summary = (
        df.groupby("venue")
        .agg(
            matches=("match_id", "count"),
            toss_win_match_win=("toss_match_win", "sum")
        )
        .reset_index()
    )

    venue_summary["toss_win_match_loss"] = (
        venue_summary["matches"] - venue_summary["toss_win_match_win"]
    )

    venue_summary["win_pct"] = (
        venue_summary["toss_win_match_win"] /
        venue_summary["matches"] * 100
    )

    venue_summary["loss_pct"] = (
        venue_summary["toss_win_match_loss"] /
        venue_summary["matches"] * 100
    )

    # restrict to top venues
    top_venues = (
        venue_summary
        .sort_values("matches", ascending=False)
        .head(top_n)["venue"]
    )

    venue_summary = venue_summary[
        venue_summary["venue"].isin(top_venues)
    ]

    return venue_summary.sort_values("matches", ascending=False)