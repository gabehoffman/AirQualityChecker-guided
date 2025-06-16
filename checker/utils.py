import requests

def geocode_location(city, state, country):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "city": city,
        "state": state,
        "country": country or "USA",
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "AirQualityChecker/1.0 (contact@example.com)"}
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return float(lat), float(lon)
        return None
    except Exception:
        return None

def fetch_air_quality(lat, lon):
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "timezone": "auto"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
