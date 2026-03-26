from . import main
import requests
import os
from datetime import datetime

#####################
# WEATHER SERVICE
#####################

def get_forecast(city="Macheke"):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Missing WEATHER_API_KEY")
        return []

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print("Weather API error:", response.text)
            return []

        data = response.json()

        forecast = []
        used_days = set()

        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            day_key = dt.strftime("%Y-%m-%d")

            if day_key not in used_days and 10 <= dt.hour <= 14:
                forecast.append({
                    "day": dt.strftime("%A"),
                    "date": dt.strftime("%d %b"),  # 👈 NEW
                    "temp": item["main"]["temp"],
                    "weather": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                })
                used_days.add(day_key)

        return forecast[:5]

    except Exception as e:
        print("Weather error:", e)
        return []