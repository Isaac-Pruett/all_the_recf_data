import pandas as pd


# The average win percentage of a team’s opponents, based on the games they’ve played in the dataset.
def get_str_schedule(df):
    # Calculate team win % first
    team_records = (
        df.groupby("team_name")["result"].value_counts().unstack(fill_value=0)
    )

    # Ensure all three columns exist
    for col in ["win", "loss", "tie"]:
        if col not in team_records.columns:
            team_records[col] = 0

    team_records["games"] = (
        team_records["win"] + team_records["loss"] + team_records["tie"]
    )
    team_records["win_pct"] = team_records["win"] / team_records["games"]

    # Build opponent list per team
    team_sos = {}

    for team, matches in df.groupby("team_name"):
        opps = []
        for match_id in matches["match_id"].unique():
            match = df[df["match_id"] == match_id]
            opps.extend(match.loc[match["team_name"] != team, "team_name"].tolist())

        # Opponents' average win %
        if opps:
            sos = team_records.loc[opps, "win_pct"].mean()
        else:
            sos = 0
        team_sos[team] = sos

    sos_df = pd.DataFrame.from_dict(
        team_sos, orient="index", columns=["strength_of_schedule"]
    )
    sos_df = sos_df.sort_values("strength_of_schedule", ascending=False)

    return sos_df


if __name__ == "__main__":
    print(get_str_schedule(pd.read_csv("savedata/matches_2024_2025.csv")))
