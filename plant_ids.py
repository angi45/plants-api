import http.client
import json

conn = http.client.HTTPSConnection("house-plants2.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "2aeb5596e5msha228838b62e03b9p107081jsn1fcd20e10a5d",
    "x-rapidapi-host": "house-plants2.p.rapidapi.com"
}

conn.request("GET", "/all-lite", headers=headers)

res = conn.getresponse()
data = res.read()

plants = json.loads(data.decode("utf-8"))

ids = [plant["id"] for plant in plants if "id" in plant]

with open("data/plant_ids.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "total": len(ids),
            "ids": ids
        },
        f,
        indent=2,
        ensure_ascii=False
    )

