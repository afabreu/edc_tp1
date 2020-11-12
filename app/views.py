from django.contrib import messages
from django.shortcuts import render
from datetime import datetime

# URL to Weather XML:
# http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072

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
    # TODO 1 function to get xml from location_id
    # TODO 2 function to get data structure from xml
    # TODO 3 tparams getting info from data_dict
    tparams = {
        'title': f'Meteorologia - {str(datetime.now().day)}',
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


def data_dict(xml):
    '''
    TODO 2: this function
    :param xml:
    :return: dict with weather parameters (same format of tparams)
    '''
    return dict()


def local_id(str):
    '''
    TODO 4
    :param str: string with the name of the city
    :return: int being the id of the input city
    '''
    return 2742611
