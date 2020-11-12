from django.contrib import messages
from django.shortcuts import render
from datetime import datetime

# URL to Weather XML: http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072
# Create your views here.
def home(request):
    if 'location' in request.POST:
        location_str = request.POST['location']
        if location_str == "":
            messages.warning(request, 'Empty search! Default location shown')
            location_str = 'Aveiro'
    else:
        location_str = 'Aveiro'
    location_id = local_id(location_str)
    tparams = {
        'title': 'Meteorologia - '+ str(datetime.now().day),
        'year': datetime.now().year,
        'location': location_id,
        'symbol': "04d",
        'precipitation': 0,
        'windDirection': "East-southeast",
        'windSpeed': 2.42,
        'temperature': 12.5,
        'feels_like': 10.91,
        'pressure': 1023,
        'humidity': 86,
        'clouds': 'overcast clouds',
        'visibility': 10000,
    }
    return render(request, 'index.html', tparams)

def local_id(str):
    return 2742611