from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.http import HttpResponse
import json
# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4fcdcff335132e39c6b7fd00b04903da'
    form = CityForm(request.POST)
    if request.method == 'POST':
        if form.is_valid() and requests.get(url.format(request.POST["name"])):
            form.save()
        
    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
                }

        weather_data.append(city_weather)
        context = {
            'weather_data':weather_data,
            'form':form,
        }
    
    return render(request,'weather/weather.html',context=context)
   