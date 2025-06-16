from django.shortcuts import render
from .forms import LocationForm
from .utils import geocode_location, fetch_air_quality


def location_view(request):
    context = {"form": LocationForm(), "submitted": False, "error": None}
    if request.method == "POST":
        form = LocationForm(request.POST)
        context["form"] = form
        context["submitted"] = False
        context["error"] = None
        if form.is_valid():
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            country = form.cleaned_data.get("country")
            coords = geocode_location(city, state, country)
            if not coords:
                context["error"] = "Location not found"
            else:
                lat, lon = coords
                aq_data = fetch_air_quality(lat, lon)
                if not aq_data or "hourly" not in aq_data:
                    context["error"] = "No recent air quality data available."
                else:
                    # Get the latest available AQI and details (find the most recent non-None value)
                    hourly = aq_data["hourly"]
                    times = hourly.get("time", [])
                    aqi = hourly.get("us_aqi", [])
                    pm25 = hourly.get("pm2_5", [])
                    pm10 = hourly.get("pm10", [])
                    ozone = hourly.get("ozone", [])
                    latest_idx = None
                    # Find the latest index with a non-None AQI value
                    if times and aqi:
                        for i in range(len(times) - 1, -1, -1):
                            if aqi[i] is not None:
                                latest_idx = i
                                break
                        if latest_idx is not None:
                            context["aqi"] = aqi[latest_idx]
                            context["measurement_time"] = times[latest_idx]
                            context["pm2_5"] = pm25[latest_idx] if pm25 and len(pm25) > latest_idx else None
                            context["pm10"] = pm10[latest_idx] if pm10 and len(pm10) > latest_idx else None
                            context["ozone"] = ozone[latest_idx] if ozone and len(ozone) > latest_idx else None
                            context["submitted"] = True
                        else:
                            context["error"] = "No recent air quality data available."
                            context["submitted"] = False
                    else:
                        context["error"] = "No recent air quality data available."
                        context["submitted"] = False
    # DEBUG: Print context for test troubleshooting
    import sys
    print('DEBUG CONTEXT:', context, file=sys.stderr)
    return render(request, "checker/location_form.html", context)
