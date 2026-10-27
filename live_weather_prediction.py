
import requests
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# 1. Load the new trained model and feature list
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_landslide.pkl"
FEATURE_PATH = BASE_DIR / "models" / "landslide_features.pkl"

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)

# --------------------------------------------------
# 2. Location: Shillong, Meghalaya
# --------------------------------------------------

latitude = 25.5788
longitude = 91.8933

# --------------------------------------------------
# 3. Fetch current weather
# --------------------------------------------------

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "precipitation"
    ),
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

current = response.json()["current"]

temperature = current["temperature_2m"]
humidity = current["relative_humidity_2m"]
rainfall = current["precipitation"]
month = datetime.now().month

# --------------------------------------------------
# 4. Prepare all 8 model features
# --------------------------------------------------
# Current precipitation is not the same as 3-day/7-day
# accumulated rainfall. Fetch recent daily weather too.

history_params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": "precipitation_sum",
    "past_days": 7,
    "forecast_days": 1,
    "timezone": "Asia/Kolkata"
}

history_response = requests.get(
    url, params=history_params, timeout=20
)
history_response.raise_for_status()

daily = history_response.json()["daily"]
daily_dates = daily["time"]
daily_rain = daily["precipitation_sum"]

today = datetime.now().date().isoformat()

# Use only completed days before today for the rainfall
# history, so today's partial rainfall is not counted twice.
past_rain = [
    value for date, value in zip(daily_dates, daily_rain)
    if date < today and value is not None
]

if len(past_rain) < 7:
    raise ValueError(
        "Not enough complete daily rainfall data to calculate "
        "7-day rainfall. Please try again later."
    )

rainfall_3day = sum(past_rain[-3:])
rainfall_7day = sum(past_rain[-7:])

input_values = {
    "latitude": latitude,
    "longitude": longitude,
    "rainfall_event_day_mm": rainfall,
    "rainfall_3day_mm": rainfall_3day,
    "rainfall_7day_mm": rainfall_7day,
    "temperature_c": temperature,
    "humidity_percent": humidity,
    "month": month
}

input_data = pd.DataFrame([input_values])[feature_columns]

# --------------------------------------------------
# 5. Predict
# --------------------------------------------------

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# This is an experimental model score, not a validated
# real-world landslide probability or official warning.
risk = "MODEL FLAG: REVIEW CONDITIONS" if prediction == 1 \
    else "NO MODEL FLAG"

# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\n" + "=" * 50)
print(" EXPERIMENTAL LANDSLIDE MODEL")
print("=" * 50)

print("Location             : Shillong, Meghalaya")
print(f"Temperature          : {temperature:.1f} °C")
print(f"Humidity             : {humidity:.0f}%")
print(f"Current precipitation: {rainfall:.1f} mm")
print(f"Previous 3-day rain  : {rainfall_3day:.1f} mm")
print(f"Previous 7-day rain  : {rainfall_7day:.1f} mm")
print(f"Month                : {month}")

print("-" * 50)
print(f"Model output         : {risk}")
print(f"Unvalidated score    : {probability * 100:.1f}%")
print("Not an official landslide warning.")
print("=" * 50)
