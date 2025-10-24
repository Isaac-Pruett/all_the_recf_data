import pandas as pd

def get_win_loss_cts(df):
    

    # Count wins and losses per team
    team_stats = df.groupby("team_name")["result"].value_counts().unstack(fill_value=0)


    # Ensure all three columns exist
    for col in ["win", "loss", "tie"]:
        if col not in team_stats.columns:
            team_stats[col] = 0

    # Compute win/loss ratio
    team_stats["win_loss_ratio"] = team_stats["win"] / team_stats["loss"].replace(0, 1)  # avoid division by zero



    #add total num of matches
    team_stats["total_matches"] = team_stats["loss"] + team_stats["win"] + team_stats["tie"]


    # Sort by win/loss ratio
    team_stats = team_stats.sort_values(by="win_loss_ratio", ascending=False)

    # Reorder columns
    team_stats = team_stats[["win", "loss", "tie", "win_loss_ratio", "total_matches"]]
    
    return team_stats

if __name__ == "__main__":
    df = pd.read_csv("savedata/matches_2024_2025.csv")
    team_stats = get_win_loss_cts(df)

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)



    print(team_stats)
