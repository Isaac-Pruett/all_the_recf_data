from str_schedule import get_str_schedule
from teamdata import teamdata_season_log, constrain_to_event
from win_loss_ratio import get_win_loss_cts
from elo import get_elo
import plotly.express as px

#EVENT_ID = 55623 #CPSLO OPEN 2025
EVENT_ID = 58911 #Worlds 2025
#EVENT_ID = None
#EVENT_ID = 53692 #worlds 2024

log = teamdata_season_log(2024, 2025, "VURC")

log = constrain_to_event(log, EVENT_ID)

stren = get_str_schedule(log)
elo = get_elo(log)
kda = get_win_loss_cts(log)

combined = kda.join(elo.join(stren))

# reset index to bring team_name into a column
combined = combined.reset_index()

# merge division column from log
combined = combined.merge(
    log[["team_name", "division"]].drop_duplicates(),
    on="team_name",
    how="left"
)

fig = px.scatter(
    combined,
    x="strength_of_schedule",
    y="elo",
    text="team_name",
    size="win_loss_ratio",
    color="division",  # now you can use division as a color or other grouping
    title=f"Elo vs Strength of Schedule Worlds {2024}-{2025}"
)

fig.update_traces(textposition="top center")
fig.show()
