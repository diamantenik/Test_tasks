import httpx
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

city_stats = {}

def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    try:
        r = httpx.get(url, params=params, timeout=5)
        data = r.json()
        if data.get("results"):
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
    except Exception as e:
        print("Ошибка геокодинга:", e)
    return None, None

def get_weather(city):
    lat, lon = get_coordinates(city)
    if not lat or not lon:
        return None
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    try:
        r = httpx.get(url, params=params, timeout=5)
        return r.json()
    except Exception as e:
        print("Ошибка запроса погоды:", e)
        return None

def home(request):
    weather_data = None
    city = ""
    error = None
    last_city = request.COOKIES.get("last_city")

    if request.method == "POST":
        city = request.POST.get("city")
        request.session.setdefault("history", []).append(city)
        request.session.modified = True

        city_stats[city] = city_stats.get(city, 0) + 1

        weather_data = get_weather(city)
        if weather_data is None:
            error = f"Город '{city}' не найден"

    context = {
        "weather": weather_data,
        "last_city": city or last_city,
        "history": request.session.get("history", []),
        "error": error,
    }

    response = render(request, "home.html", context)
    if city:
        response.set_cookie("last_city", city)
    return response

def history(request):
    history = request.session.get("history", [])
    return render(request, "history.html", {"history": history})

@csrf_exempt
def stats_api(request):
    return JsonResponse(city_stats)
