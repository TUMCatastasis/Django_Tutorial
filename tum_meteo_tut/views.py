from datetime import datetime

import json
import geocoder as geocoder
import requests
from django.http import HttpResponse, JsonResponse
from django.template import loader
from tum_meteo_tut.models import Worldcities


# all_cities = [cityData.city for cityData in Worldcities.objects.all()]

# print(all_cities)

def find_city(request):
    city = request.GET.get('city')
    payload = []
    if city:
        city_objs = Worldcities.objects.filter(city__icontains=city)
        payload = [cityData.city for cityData in city_objs]

    return JsonResponse({'status': 200, 'data': payload})


def display_info(request, city, city_temp, country, lat, lng):
    template = loader.get_template('index.html')
    context = {
        'city': city,
        'temp': city_temp,
        'country': country,
        'lat': lat,
        'lng': lng
    }

    return HttpResponse(template.render(context, request))


def search(request):
    cityData = Worldcities.objects.filter(city__icontains=request.GET.get('city')).first()
    city = cityData.city
    location = [cityData.lat, cityData.lng]
    temp = get_temp(location)
    country = cityData.country

    return display_info(request, city, temp, country, cityData.lat, cityData.lng)


def temp_here(request):
    loc_info = geocoder.ipinfo('me')
    loc = loc_info.latlng
    temp = get_temp(loc)
    city = loc_info.city
    country_code = loc_info.country

    with open("tum_meteo_tut/country_codes.json") as json_file:
        json_data = json.load(json_file)
        country = json_data[country_code] or country_code

    return display_info(request, f"Your Location ({city})", temp, country, loc_info.lat, loc_info.lng)


def temp_somewhere(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    city = random_item.city
    country = random_item.country
    location = [random_item.lat, random_item.lng]
    temp = get_temp(location)
    return display_info(request, city, temp, country, random_item.lat, random_item.lng)


def get_temp(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    return temp
