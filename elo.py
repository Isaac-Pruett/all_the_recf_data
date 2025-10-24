import pandas as pd

import pandas as pd

def get_elo(df, k=32, base_rating=1500):
    # Initialize ratings
    ratings = {team: base_rating for team in df["team_name"].unique()}

    # Sort matches by match_id (assuming chronological order)
    for match_id, match in df.groupby("match_id"):
        teams = match["team_name"].tolist()
        results = match["result"].tolist()

        if len(teams) != 2:
            continue  # skip malformed matches

        team_a, team_b = teams
        result_a, result_b = results

        # Map result to score (win=1, tie=0.5, loss=0)
        score_map = {"win": 1, "tie": 0.5, "loss": 0}
        S_a = score_map[result_a]
        S_b = score_map[result_b]

        R_a = ratings[team_a]
        R_b = ratings[team_b]

        # Expected scores
        E_a = 1 / (1 + 10 ** ((R_b - R_a) / 400))
        E_b = 1 - E_a

        # Update ratings
        ratings[team_a] = R_a + k * (S_a - E_a)
        ratings[team_b] = R_b + k * (S_b - E_b)

    # Convert to DataFrame
    team_stats = pd.DataFrame.from_dict(ratings, orient="index", columns=["elo"])
    team_stats = team_stats.sort_values("elo", ascending=False)

    return team_stats



if __name__ == "__main__":
    from teamdata import teamdata_season_log
    EVENT_ID = None
    log = teamdata_season_log(2024, 2025, "VURC")

    if EVENT_ID:
        log = log[log['event_id'] == EVENT_ID]

    elo = get_elo(log)

    print(elo.head(20))