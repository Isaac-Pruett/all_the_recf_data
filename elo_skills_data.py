import argparse
from this import s

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

combined = kda.join(elo.join(stren))

# reset index to bring team_name into a column
combined = combined.reset_index()

# merge division column from log
combined = combined.merge(
    mlog[["team_name", "division"]].drop_duplicates(), on="team_name", how="left"
)


print(slog.columns)
print(mlog.columns)
