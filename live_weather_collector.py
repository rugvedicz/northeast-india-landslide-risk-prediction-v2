
import requests
import json
import time
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(
    BASE_DIR, "data", "live_weather_stream.json"
)

locations = {
    "Itanagar": {
        "state": "Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053
    },
    "Dispur": {
        "state": "Assam",
        "latitude": 26.1433,
        "longitude": 91.7898
    },
    "Imphal": {
        "state": "Manipur",
        "latitude": 24.8170,
        "longitude": 93.9368
    },
    "Shillong": {
        "state": "Meghalaya",
        "latitude": 25.5788,
        "longitude": 91.8933
    },
    "Aizawl": {
        "state": "Mizoram",
        "latitude": 23.7271,
        "longitude": 92.7176
    },
    "Kohima": {
        "state": "Nagaland",
        "latitude": 25.6751,
        "longitude": 94.1086
    },
    "Gangtok": {
        "state": "Sikkim",
        "latitude": 27.3389,
        "longitude": 88.6065
    },
    "Agartala": {
        "state": "Tripura",
        "latitude": 23.8315,
        "longitude": 91.2868
    }
}

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

session = requests.Session()

while True:
    for location_name, location_data in locations.items():
        latitude = location_data["latitude"]
        longitude = location_data["longitude"]

        try:
            # Current weather
            current_response = session.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "precipitation"
                    ),
                    "timezone": "Asia/Kolkata"
                },
                timeout=20
            )
            current_response.raise_for_status()
            current = current_response.json()["current"]

            # Recent daily rainfall
            history_response = session.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "daily": "precipitation_sum",
                    "past_days": 7,
                    "forecast_days": 1,
                    "timezone": "Asia/Kolkata"
                },
                timeout=20
            )
            history_response.raise_for_status()
            daily = history_response.json()["daily"]

            today = datetime.now().date().isoformat()

            # Exclude today's incomplete daily total.
            completed_rain = [
                value
                for date, value in zip(
                    daily["time"],
                    daily["precipitation_sum"]
                )
                if date < today and value is not None
            ]

            if len(completed_rain) < 7:
                raise ValueError(
                    "Not enough completed daily rainfall values"
                )

            rainfall_3day = sum(completed_rain[-3:])
            rainfall_7day = sum(completed_rain[-7:])

            now = datetime.now()

            record = {
                "timestamp": now.isoformat(),
                "location": location_name,
                "state": location_data["state"],
                "latitude": latitude,
                "longitude": longitude,
                "rainfall_mm": current["precipitation"],
                "rainfall_event_day_mm": current["precipitation"],
                "rainfall_3day_mm": rainfall_3day,
                "rainfall_7day_mm": rainfall_7day,
                "temperature_c": current["temperature_2m"],
                "humidity_percent": current["relative_humidity_2m"],
                "month": now.month
            }

            with open(
                OUTPUT_FILE, "a", encoding="utf-8"
            ) as file:
                file.write(json.dumps(record) + "\n")

            print(
                f"OK {location_name} | "
                f"Temp: {current['temperature_2m']} C | "
                f"Humidity: {current['relative_humidity_2m']}% | "
                f"Current precipitation: {current['precipitation']} mm | "
                f"3-day rain: {rainfall_3day:.1f} mm | "
                f"7-day rain: {rainfall_7day:.1f} mm"
            )

        except Exception as error:
            print(f"Error for {location_name}: {error}")

    print("\nWaiting 10 minutes...\n")
    time.sleep(600)
