from recf_api import load_data_from


def get_events(season_id):
    return load_data_from(f"/seasons/{season_id}/events")

if __name__ == "__main__":
    get_events(198)


def get_matches(team_id, season_id):
    return load_data_from(f"/teams/{team_id}/matches?season={season_id}")



if __name__ == "__main__":
    get_matches(106975, 191)


def get_teams(event_id):
    return load_data_from(f"/events/{event_id}/teams")

if __name__ == "__main__":
    get_teams(55623)


def get_season_by_year(start, end, code):
    md = load_data_from("/seasons")
    start, end = int(start), int(end)   # ensure numeric
    #print(f"getting season: {start}-{end} for {code}")
    for d in md["data"]:
        #print(f"{d['name']}, id={d['id']}, {d['years_start']}-{d['years_end']}, code={d['program']['code']}")
        if d['program']['code'] == code and (d['years_start'] == start or d['years_end'] == end):
            print(d['name'])
            return d['id']
    raise RuntimeError(f"{code} season {start}-{end} not found.")
        
def get_season_by_name(name, code):
    md = load_data_from("/seasons")
    lowername = name.lower()
    #print(f"getting season: {start}-{end} for {code}")
    for d in md["data"]:
        #print(f"{d['name']}, id={d['id']}, {d['years_start']}-{d['years_end']}, code={d['program']['code']}")
        if d['program']['code'] == code and (d['name'].lower().endswith(lowername)):
            print(d['name'])
            return d['id']
    raise RuntimeError(f"{code} season {name} not found.")

if __name__ == "__main__":
    get_season_by_name("High Stakes", "VURC")

if __name__ == "__main__":
    get_season_by_year(2025, 2026, 'VURC')



def get_programs():
    return load_data_from("/programs")


if __name__ == "__main__":
    get_programs()



def get_id_list(data):
    l = []
    try:
        for i in data["data"]:
            l.append(i["id"])
    except Exception as e:
        raise

    return l