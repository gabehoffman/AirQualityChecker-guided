from django import template

register = template.Library()

@register.filter
def aqi_advisory(aqi):
    try:
        aqi = int(aqi)
    except (TypeError, ValueError):
        return "No advisory available."
    if aqi <= 50:
        return "Good: Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate: Acceptable air quality."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups."
    elif aqi <= 200:
        return "Unhealthy: Everyone may begin to experience health effects."
    elif aqi <= 300:
        return "Very Unhealthy: Health alert."
    else:
        return "Hazardous: Health warnings of emergency conditions."
