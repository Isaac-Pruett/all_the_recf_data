import requests
import json
import os
import time

base_url = "https://www.robotevents.com/api/v2"

with open("pass.txt", "r") as f:
    passkey = f.read().strip()

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {passkey}",
}

iterationcount = 1

def get_data_from(location):
    url = base_url + location + "?per_page=250"
    data = None
    global iterationcount

    while data is None or (isinstance(data, dict) and data.get("message") == "Too Many Attempts."):
        response = requests.get(url, headers=headers)
        print("GET", url, "->", response.status_code)
        

        if response.status_code == 429:
            print("Too many requests. Suspending... Please wait.")
            time.sleep(5 * iterationcount)
            iterationcount += 1
            continue

        iterationcount = 1

        try:
            data = response.json()
        except Exception as e:
            print("Error parsing JSON:", e)
            print("Response text:", response.text)
            raise

        #time.sleep(0.5)
            

        

    if "meta" not in data:
        raise ValueError(f"Unexpected response at {url}: {data}")

    return data



def load_data_from(location):
    output_path = f"./data{location}.json"

    if not os.path.exists(output_path):
        metadata = get_data_from(location)
        page_count = metadata["meta"]["last_page"]

        for i in range(2, page_count + 1):  # start at page 2
            page = f"{location}?page={i}"
            new_md = get_data_from(page)
            metadata["data"].extend(new_md["data"])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(metadata, f, indent=4)

        return metadata
    else:
        with open(output_path, "r") as f:
            return json.load(f)


if __name__ == "__main__":
    # VURC 2024–2025 = season_id 175
    events = load_data_from("/seasons/175/events")
    print(f"Loaded {len(events['data'])} events.")
