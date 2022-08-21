import requests
from datetime import datetime as dt
import os

GENDER = "Male"
WEIGHT_KG = 74
HEIGHT_CM = 174
AGE = 34


APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/6ae5568f6e97ca5e4bca9033a094bbff/workoutTracking/workouts"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()


today_date = dt.now().strftime("%d/%m/%Y")
now_time = dt.now().strftime("%X")


for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "calories": exercise["nf_calories"],
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],

        }
    }


sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=("darkwing", "duck"))

print(sheet_response.text)

