import re
from collectionutils import *
import pandas as pd
import folium


if __name__ == "__main__":
 
    years = input("Enter year range: ")
    years_list = [y.strip() for y in re.split(r"[ ,\-_]+", years) if y.strip()]
    if (len(years_list) != 2):
        raise ValueError("Enter a valid year range: (ex: 2024-2025)")
    start, end = years_list


    program_name = input("Enter program name: ")

    all_programs = load_data_from("/programs")["data"]
    prog_id = None
    #print(program_name)


    for p in all_programs:
        #print(p["abbr"])
        if program_name.lower() == "vexu":
            prog_id = "VURC"
            break

        if program_name.lower() in [p["abbr"].lower(), p["name"].lower()]:
            prog_id = p["abbr"]
            break
    
    if not prog_id:
        raise RuntimeError("The program could not be found")
    
    season_id = get_season_by_year(start, end, prog_id)

    events_md = get_events(season_id)
    
    

    # Extract relevant data
    event_list = []
    for event in events_md["data"]:
        loc = event.get("location", {})
        coords = loc.get("coordinates", {})
        if coords.get("lat") and coords.get("lon"):
            event_list.append({
                "name": event["name"],
                "venue": loc.get("venue"),
                "city": loc.get("city"),
                "state": loc.get("region"),
                "country": loc.get("country"),
                "lat": coords.get("lat"),
                "lon": coords.get("lon"),
                "start": event.get("start"),
                "end": event.get("end")
            })

    # Convert to DataFrame
    df_events = pd.DataFrame(event_list)
    print(df_events.head())

    # Create interactive map
    m = folium.Map(
        location=[df_events['lat'].mean(), df_events['lon'].mean()],
        zoom_start=4
    )

    # Add event markers
    for _, row in df_events.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=(f"{row['name']}\n{row['venue']}\n{row['city']}, {row['state']}, {row['country']}"
                   f"\n{row['start']} - {row['end']}")
        ).add_to(m)

    # Save map
    fn = f"data/maps/events_map_{start}_{end}_{prog_id}.html"
    m.save(fn)
    print(f"Map saved as {fn}")