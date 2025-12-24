import argparse

import plotly.express as px

from metrics.elo import get_elo
from metrics.str_schedule import get_str_schedule
from metrics.win_loss_ratio import get_win_loss_cts
from teamdata import matches_log

p = argparse.ArgumentParser()

p.add_argument("start")
p.add_argument("end")
p.add_argument("code")

args = p.parse_args()

log = matches_log(int(args.start), int(args.end), args.code.upper())

stren = get_str_schedule(log)
elo = get_elo(log)
kda = get_win_loss_cts(log)

combined = kda.join(elo.join(stren))

# reset index to bring team_name into a column
combined = combined.reset_index()

# merge division column from log
combined = combined.merge(
    log[["team_name", "division"]].drop_duplicates(), on="team_name", how="left"
)

fig = px.scatter(
    combined,
    x="strength_of_schedule",
    y="elo",
    text="team_name",
    size="win_loss_ratio",
    color="division",  # now you can use division as a color or other grouping
    title=f"Elo vs Strength of Schedule ---{args.code.upper()}--- {args.start}-{args.end}",
    # title=f"Elo vs Strength of Schedule ------ {next((e for e in get_events(get_season_by_year(2025, 2026, 'VURC'))['data'] if e['id'] == EVENT_ID))['name']}",
)

fig.update_traces(textposition="top center")
fig.show()
