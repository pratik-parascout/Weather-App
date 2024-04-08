from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def index(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Kolkata'
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='
    PARAMS = {'units':'metric'}
    API_KEY = ''
    SEARCH_ENGINE_ID = ''

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    search_type = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"
    
    try:
        weather_response = requests.get(url, params=PARAMS)
        weather_response.raise_for_status()  # Raise an exception for HTTP errors
        weather_data = weather_response.json()

        description = weather_data['weather'][0]['description'].upper()
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        search_response = requests.get(city_url)
        search_response.raise_for_status()
        search_data = search_response.json()
        search_items = search_data.get("items", [])
        if search_items:
            image_url = search_items[0]['link']  # Get the first image URL
        else:
            image_url = None

        return render(request, 'core/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occured': False,
            'image_url': image_url
        })
    
    except requests.RequestException as e:
        messages.error(request, f'Error: {e}')
        return render(request, 'core/index.html', {
            'description': 'Thunderstorm',
            'icon': '10d',
            'temp': 20,
            'day': datetime.date.today(),
            'city': 'Mars',
            'exception_occured': True,
            'image_url': None
        })
