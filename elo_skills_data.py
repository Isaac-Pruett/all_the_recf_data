import argparse

import plotly.express as px

from metrics.elo import get_elo
from metrics.str_schedule import get_str_schedule
from metrics.win_loss_ratio import get_win_loss_cts
from teamdata import matches_log, skills_log

p = argparse.ArgumentParser()

p.add_argument("start")
p.add_argument("end")
p.add_argument("code")

args = p.parse_args()

slog = skills_log(int(args.start), int(args.end), args.code.upper())

mlog = matches_log(int(args.start), int(args.end), args.code.upper())

stren = get_str_schedule(mlog)
elo = get_elo(mlog)
kda = get_win_loss_cts(mlog)

matches_metrics = kda.join(elo.join(stren))

# reset index to bring team_name into a column
matches_metrics = matches_metrics.reset_index()

# merge division column from log
matches_metrics = matches_metrics.merge(
    mlog[["team_name", "division"]].drop_duplicates(), on="team_name", how="left"
)

skills_best = (
    slog.groupby(["team_id", "team_name", "type"], as_index=False)["score"]
    .max()  # or .first() if you want the first attempt
    .pivot(index=["team_id", "team_name"], columns="type", values="score")
    .reset_index()
    .rename(columns={"driver": "driver_skills", "programming": "programming_skills"})
)

# Optional: fill missing skills with 0 (or NaN if you prefer)
skills_best = skills_best.fillna(0)

print(skills_best.head(10))
print(matches_metrics.head(10))


# Final combined DataFrame with skills + match stats
final_df = matches_metrics.merge(
    skills_best[["team_name", "driver_skills", "programming_skills"]],
    on="team_name",
    how="left",  # keep all teams from combined, even if no skills data
)

# Optional: fill missing skills scores with 0 (common in robotics rankings)
final_df["driver_skills"] = final_df["driver_skills"].fillna(0)
final_df["programming_skills"] = final_df["programming_skills"].fillna(0)

# Optional: round some numeric columns for cleaner display
final_df = final_df.round({"elo": 1, "strength_of_schedule": 3, "win_loss_ratio": 2})

# Sort by ELO descending (most common way to present rankings)
final_df = final_df.sort_values("elo", ascending=False)

print(final_df.head(15))


fig = px.scatter(
    final_df,
    x="strength_of_schedule",
    y="elo",
    text="team_name",
    size="programming_skills",
    color="driver_skills",
    title=f"Elo vs Strength of Schedule, Skills Scores (Driver = Color, Programming = Size) ---{args.code.upper()}--- {args.start}-{args.end}",
    # title=f"Elo vs Strength of Schedule ------ {next((e for e in get_events(get_season_by_year(2025, 2026, 'VURC'))['data'] if e['id'] == EVENT_ID))['name']}",
)

fig.update_traces(textposition="top center")
fig.show()
