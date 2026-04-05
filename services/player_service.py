import pandas as pd

def get_players_per_season(df):

    # Batter
    batters = df[["year", "batter"]].rename(columns={"batter": "player"})

    # Bowler
    bowlers = df[["year", "bowler"]].rename(columns={"bowler": "player"})

    # Non-striker
    non_strikers = df[["year", "non_striker"]].rename(columns={"non_striker": "player"})

    # Fielders
    fielders = (
        df[["year", "fielders"]]
        .dropna()
        .assign(player=lambda x: x["fielders"].str.split(","))
        .explode("player")
        .assign(player=lambda x: x["player"].str.strip())
        [["year", "player"]]
    )

    all_players = pd.concat(
        [batters, bowlers, non_strikers, fielders],
        ignore_index=True
    ).dropna(subset=["player"])

    players_per_season = (
        all_players
        .drop_duplicates()
        .groupby("year")["player"]
        .nunique()
        .reset_index(name="total_players")
        .sort_values("year")
    )

    return players_per_season