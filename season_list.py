from recf_api import load_data_from


def list_seasons():
    md = load_data_from("/seasons")
    list = []
    for d in md["data"]:
        list.append(f"{d['name']}, id={d['id']}, {d['years_start']}-{d['years_end']}")
    return list


if __name__ == "__main__":
    l = list_seasons()
    for i in l:
        print(i)

    # get_season_by_year(2025, 2026, 'VURC')
