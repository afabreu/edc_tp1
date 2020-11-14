from django.contrib import messages
from django.shortcuts import render
from datetime import datetime
from app import basex_actions
import json
import edc_tp1.settings
import xmltodict
import requests

# URL to Weather XML:
# http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072

# Create your views here.

cities = {}

with open(edc_tp1.settings.CITIES_JSON) as f:
    json_data = json.loads(f.read())
    for jd in json_data:
        cities[jd['name']] = jd['id']


def home(request):
    if 'local' in request.POST:
        location_str = request.POST['local']
        if location_str == "":
            messages.warning(request, 'Empty search! Default location shown')
            location_str = 'Aveiro'
    else:
        location_str = 'Aveiro'
    location_str, location_id = local_id(location_str)
    # TODO create db
    # TODO f1 basex_actions.db_to_xml to get xml from db name and location_str
    # TODO tparams getting info from data_dict
    tparams = {
        'title': f'Meteorologia - {datetime.now().day}/{datetime.now().month}',
        'year': datetime.now().year,
        'location': f'{location_str} - {location_id}',
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


def api_call(city_id: int, key: str = 'd0279fea67692adea0e260e4cf86d072'):
    """

    :param city_id:
    :param key: api key
    :return:
    """

    # http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072
    url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&units=metric&mode=xml&APPID={key}"

    request = requests.get(url=url)
    assert request.status_code == 200, f"Request error! Status {request.status_code}"

    xml = request.content.decode(request.encoding)
    return xml


def data_dict(xml):
    """
    :param xml: xml with weather data of the city
    :return: dict with weather parameters (same format of tparams)
    """
    d = xmltodict.parse(xml)
    # TODO d is an OrderedDict, we may need to change to a simple dict
    return d


def local_id(str):
    '''
    :param str: string with the name of the city
    :return: int being the id of the input city
    '''
    if str == "Lisboa":
        city_name = "Lisbon"
    else:
        city_name = str
    return (city_name, cities.get(city_name, 8010417))
