from recf_api import load_data_from

from collectionutils import get_season_by_year
            

        


if __name__ == "__main__":

    md = load_data_from("/seasons")

    for d in md["data"]:
        print(f"{d['name']}, id={d['id']}, {d['years_start']}-{d['years_end']}")

    #get_season_by_year(2025, 2026, 'VURC')

