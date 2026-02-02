import http.client
import json
import time

API_HOST = "house-plants2.p.rapidapi.com"
API_KEY = "2aeb5596e5msha228838b62e03b9p107081jsn1fcd20e10a5d"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

with open("data/plant_ids.json", "r", encoding="utf-8") as f:
    ids_data = json.load(f)

plant_ids = ids_data["ids"]

all_plants = []

conn = http.client.HTTPSConnection(API_HOST)

for i, plant_id in enumerate(plant_ids, start=1):
    print(f"[{i}/{len(plant_ids)}] Fetching plant ID: {plant_id}")

    conn.request("GET", f"/id/{plant_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        plant_data = json.loads(data.decode("utf-8"))
        all_plants.append(plant_data)

    time.sleep(1)

conn.close()

with open("data/plants.json", "w", encoding="utf-8") as f:
    json.dump(all_plants, f, indent=2, ensure_ascii=False)

