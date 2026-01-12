import os
import re

import pandas as pd

from collectionutils import (
    get_events,
    get_id_list,
    get_matches,
    get_season_by_year,
    get_skills,
    get_teams,
)
from recf_api import load_data_from


def matches_log(start, end, code):  # gets all match data for an entire season
    fn = f"savedata/matches_{code}_{start}_{end}.csv"
    if not os.path.exists(fn):
        season_id = get_season_by_year(start, end, code)
        events_md = get_events(season_id)
        event_ids = get_id_list(events_md)

        rows = []

        for i in event_ids:  # event IDs
            for j in get_id_list(get_teams(i)):  # team IDs
                matches = get_matches(j, season_id)  # JSON of matches
                for match in matches.get("data", []):
                    # make a dict of color → score
                    scores = {a["color"]: a["score"] for a in match["alliances"]}

                    for alliance in match["alliances"]:
                        opp_color = "red" if alliance["color"] == "blue" else "blue"
                        result = "tie"
                        if alliance["score"] > scores[opp_color]:
                            result = "win"
                        elif alliance["score"] < scores[opp_color]:
                            result = "loss"

                        for team_entry in alliance["teams"]:
                            rows.append(
                                {
                                    "match_id": match["id"],
                                    "event_id": match["event"]["id"],
                                    "event_name": match["event"]["name"],
                                    "division": match["division"]["name"],
                                    "round": match["round"],
                                    "match_number": match["matchnum"],
                                    "scheduled": match["scheduled"],
                                    "field": match["field"],
                                    "alliance_color": alliance["color"],
                                    "alliance_score": alliance["score"],
                                    "team_id": team_entry["team"]["id"],
                                    "team_name": team_entry["team"]["name"],
                                    "result": result,
                                }
                            )

        df = pd.DataFrame(rows)

        # Drop exact duplicates
        df = df.drop_duplicates()

        # Or, if you want to ensure uniqueness by match/team pair:
        df = df.drop_duplicates(subset=["match_id", "team_id"])

        df.to_csv(fn, index=False)
        print(f"Saved {fn} with", len(df), "rows")
    else:
        df = pd.read_csv(fn)

    return df


def constrain_to_event(log, event_id):
    if event_id:
        log = log[log["event_id"] == event_id]
    return log


def skills_log(start, end, code):
    fn = f"savedata/skills_{code}_{start}_{end}.csv"
    if not os.path.exists(fn):
        season_id = get_season_by_year(start, end, code)
        events_md = get_events(season_id)
        event_ids = get_id_list(events_md)

        rows = []

        for i in event_ids:  # event IDs
            for j in get_id_list(get_teams(i)):  # team IDs
                skills = get_skills(j, season_id)  # JSON of matches
                for s in skills.get("data", []):
                    # make a dict

                    rows.append(
                        {
                            "match_id": s["id"],
                            "event_id": s["event"]["id"],
                            "event_name": s["event"]["name"],
                            "team_id": s["team"]["id"],
                            "team_name": s["team"]["name"],
                            # "division": s["division"]["name"],
                            "rank": s["rank"],
                            "type": s["type"],
                            "score": s["score"],
                            "attempts": s["attempts"],
                        }
                    )

        df = pd.DataFrame(rows)

        # Drop exact duplicates
        df = df.drop_duplicates()
        df = df.drop_duplicates(subset=["team_id", "type"])

        # Or, if you want to ensure uniqueness by match/team pair:

        df.to_csv(fn, index=False)
        print(f"Saved {fn} with", len(df), "rows")
    else:
        df = pd.read_csv(fn)

    return df


if __name__ == "__main__":
    years = input("Enter year range: ")
    years_list = [y.strip() for y in re.split(r"[ ,\-_]+", years) if y.strip()]
    if len(years_list) != 2:
        raise ValueError("Enter a valid year range: (ex: 2024-2025)")
    start, end = years_list

    program_name = input("Enter program name: ")

    all_programs = load_data_from("/programs")["data"]
    prog_id = None

    for p in all_programs:
        if program_name.lower() == "vexu":
            prog_id = "VURC"
            break
        if program_name.lower() in [p["abbr"].lower(), p["name"].lower()]:
            prog_id = p["abbr"]
            break

    if not prog_id:
        raise RuntimeError("The program could not be found")

    matches_log(start, end, prog_id)


def has_skills_log(start, end, code):
    fn = f"savedata/skills_{code}_{start}_{end}.csv"
    return os.path.exists(fn)


def has_matches_log(start, end, code):
    fn = f"savedata/matches_{code}_{start}_{end}.csv"
    return os.path.exists(fn)
