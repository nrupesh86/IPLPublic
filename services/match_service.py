import numpy as np
import pandas as pd

def build_match_df(df: pd.DataFrame) -> pd.DataFrame:

    match_columns = [
        'match_id',
        'date',
        'match_type',
        'event_name',
        'innings',
        'batting_team',
        'bowling_team',
        'match_won_by',
        'win_outcome',
        'toss_winner',
        'toss_decision',
        'venue',
        'city',
        'day',
        'month',
        'year',
        'season',
        'superover_winner',
        'event_match_no',
        'stage'
    ]

    match_df = df[match_columns].copy()

    # Derive teams
    match_df['team_1'] = np.where(
        match_df['innings'] == 1,
        match_df['batting_team'],
        match_df['bowling_team']
    )

    match_df['team_2'] = np.where(
        match_df['innings'] == 1,
        match_df['bowling_team'],
        match_df['batting_team']
    )

    # Deduplicate to match-level
    match_df = (
        match_df
        .drop_duplicates(subset="match_id")
        .reset_index(drop=True)
    )

    # Drop ball-level columns
    match_df = match_df.drop(
        columns=["batting_team", "bowling_team", "innings"],
        errors="ignore"
    )

    # Final column ordering
    match_columns_new = [
        'match_id',
        'date',
        'match_type',
        'event_name',
        'team_1',
        'team_2',
        'match_won_by',
        'win_outcome',
        'toss_winner',
        'toss_decision',
        'venue',
        'city',
        'day',
        'month',
        'year',
        'season',
        'superover_winner',
        'event_match_no',
        'stage'
    ]

    return match_df[match_columns_new]