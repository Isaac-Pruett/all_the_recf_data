# This example requires the 'message_content' intent.

import os

import discord

from metrics.elo import get_elo
from metrics.str_schedule import get_str_schedule
from teamdata import has_matches_log, has_skills_log, matches_log, skills_log

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


def process_msg_for_team(msg: str):
    d = msg.split(" ")
    teamname = d[1].upper()

    start = int(d[2]) if len(d) > 2 else 2025
    end = int(d[3]) if len(d) > 3 else 2026
    code = d[4].upper() if len(d) > 4 else "VURC"

    return teamname, start, end, code


async def get_relevant_mlog(cx: str, m: discord.Message):
    teamname, start, end, code = process_msg_for_team(cx)

    if not has_matches_log(start, end, code):
        await m.channel.send(
            f"So sorry, we don't have the match data for the {code} season from {start}-{end} on hand.\nI'll fetch it for you and send it here when I finish collecting it."
        )
    log = matches_log(start, end, code)

    return log


async def get_relevant_slog(cx: str, m: discord.Message):
    teamname, start, end, code = process_msg_for_team(cx)

    if not has_skills_log(start, end, code):
        await m.channel.send(
            f"So sorry, we don't have the skills data for the {code} season from {start}-{end} on hand.\nI'll fetch it for you and send it here when I finish collecting it."
        )
    log = skills_log(start, end, code)

    return log


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:  # dont respond to our own messages
        return
    cx = message.content
    if cx.startswith("$hello"):
        await message.channel.send("Hello! :sparkles:")
    if cx.startswith("$elo"):
        teamname, start, end, code = process_msg_for_team(cx)
        log = await get_relevant_mlog(cx, message)

        elo = get_elo(log)

        log = elo.join(log)

        if teamname not in log.index:
            await message.channel.send(
                f"Sorry, I couldn't find team `{teamname}` in {code} season {start}-{end}."
            )
            return

        elo_value = log.loc[teamname, "elo"]

        await message.channel.send(f"**{teamname} Elo:** `{elo_value:.2f}`")
    if cx.startswith("$summary"):
        try:
            teamname, start, end, code = process_msg_for_team(cx)
            mlog = await get_relevant_mlog(cx, message)
            slog = await get_relevant_slog(cx, message)
            driver_df = (
                slog[slog["type"] == "driver"]
                .set_index("team_name")
                .sort_values(by="score", ascending=False)
            )
            programming_df = (
                slog[slog["type"] == "programming"]
                .set_index("team_name")
                .sort_values(by="score", ascending=False)
            )

            elo = get_elo(mlog).sort_values(by="elo", ascending=False)

            sos = get_str_schedule(mlog).sort_values(
                by="strength_of_schedule", ascending=False
            )

            await message.channel.send(
                f"""__**Current {code} {start}-{end} data for {teamname}**__

**{teamname} elo:** `{elo.loc[teamname, "elo"]:.2f}` \t rank: `{elo.index.get_loc(teamname) + 1}`

**{teamname} strength of schedule:** `{(sos.loc[teamname, "strength_of_schedule"] * 100.0):.2f}`% \t rank: `{sos.index.get_loc(teamname) + 1}`

**{teamname} skills:**
Driver: `{driver_df.loc[teamname, "score"]}`,  rank: `{driver_df.index.get_loc(teamname) + 1}`
Programming: `{programming_df.loc[teamname, "score"]}`,  rank: `{programming_df.index.get_loc(teamname) + 1}`
"""
            )
        except KeyError as e:
            print(e)
            await message.channel.send(
                f"{teamname} appears not to have played a match yet..."
            )
    if cx.startswith("$github"):
        await message.channel.send("")

    if cx.startswith("$help"):
        await message.channel.send("""GitHub: ```$github```
Team Summary: ```$summary <team name> <start yr> <end yr> <code>``` ```$summary cpslo 2024 2025``` ```$summary cpslo```
             """)


token = os.environ["DISCORD_TOKEN"]
client.run(token)
