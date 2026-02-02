from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Монтирај ја папката assets/images за статички фајлови
app.mount("/images", StaticFiles(directory="assets/images"), name="images")

# Прочитај го локалниот JSON
with open("data/plants.json", "r", encoding="utf-8") as f:
    plants_data = json.load(f)

def smart_watering_schedule(watering_text):
    text = watering_text.lower()

    if "keep moist" in text and "can dry" in text:
        return 4
    elif "keep moist" in text and "must not dry" in text:
        return 2
    elif "water when soil is half dry" in text and "can dry" in text:
        return 7
    elif "keep moist" in text and "water when soil is half dry" in text:
        return 4
    elif "water when soil is half dry" in text and "change water regularly" in text:
        return 6
    elif "change water regularly" in text and "water when soil is half dry" in text:
        return 6
    elif "must dry" in text and "water only when dry" in text:
        return 12
    elif "water only when dry" in text and "must dry" in text:
        return 12
    elif "water when soil is half dry" in text and "water only when dry" in text:
        return 8
    elif "can dry" in text and "water when soil is half dry" in text:
        return 7
    return 5

@app.get("/plants")
async def get_plants():
    plants_with_local_id = []
    for index, plant in enumerate(plants_data, start=1):
        plant_copy = plant.copy()
        plant_copy["local_id"] = index
        plant_copy["watering_schedule"] = smart_watering_schedule(plant_copy.get("Watering", ""))

        plant_copy["thumbnail"] = f"/images/{index}.jpg"

        plants_with_local_id.append(plant_copy)

    return plants_with_local_id

@app.get("/plants/{local_id}")
async def get_plant_by_local_id(local_id: int):
    if 1 <= local_id <= len(plants_data):
        plant_copy = plants_data[local_id - 1].copy()
        plant_copy["local_id"] = local_id
        plant_copy["watering_schedule_days"] = smart_watering_schedule(plant_copy.get("Watering", ""))
        plant_copy["thumbnail"] = f"/images/{local_id}.jpg"
        return plant_copy
    return {"error": "Plant not found"}

@app.get("/categories")
async def get_categories():
    categories = sorted({plant.get("Categories") for plant in plants_data if plant.get("Categories")})
    return categories
