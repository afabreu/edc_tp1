from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, timedelta
from app import basex_actions
from lxml import etree
from BaseXClient import BaseXClient
import json
import edc_tp1.settings
import xmltodict
import requests

# URL to Weather XML:
# http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072

# Create your views here.

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

# eg: {'Aveiro': 1, 'Lisboa': 2, ...}
cities = {}

with open(edc_tp1.settings.TESTING_JSON) as f:
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
    location_str, location_id = get_local_id(location_str)
    # create or open db
    database()
    # TODO f1 basex_actions.db_to_xml to get xml from db name and location_str
    # TODO tparams getting info from data_dict
    tparams = {
        'title': f'Meteorologia - {datetime.now().day}/{datetime.now().month}',
        'year': datetime.now().year,
        'location': location_str,
        'localtion_id': location_id,
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


def forecast(request, local_id):
    now = datetime.now()  # Dia e Hora(com minutos, segundos, etc) atuais
    remove_min_sec = timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now -= remove_min_sec  # Dia e Hora(apenas hora) atuais
    hour_of_today = now.hour
    remove_hour = timedelta(hours=hour_of_today)
    today = now - remove_hour  # Dia de hoje
    hour_of_today -= (hour_of_today % 3)  # Hora atual divisível por 3 anterior
    now = today + timedelta(hours=hour_of_today)
    if 'inputDia' in request.POST and 'inputHora' in request.POST:
        dia = request.POST['inputDia']
        hora = request.POST['inputHora']

        sum_day = -1
        if dia == "Hoje":
            sum_day = timedelta(days=0)
        elif dia == "Amanhã":
            sum_day = timedelta(days=1)
        elif dia == "Daqui a 2 dias":
            sum_day = timedelta(days=2)
        elif dia == "Daqui a 3 dias":
            sum_day = timedelta(days=3)
        elif dia == "Daqui a 4 dias":
            sum_day = timedelta(days=4)
        elif dia == "Daqui a 5 dias":
            sum_day = timedelta(days=5)

        today += sum_day

        sum_hour = -1
        if hora == "00:00 - 03:00":
            sum_hour = timedelta(hours=0)
        elif hora == "03:00 - 06:00":
            sum_hour = timedelta(hours=3)
        elif hora == "06:00 - 09:00":
            sum_hour = timedelta(hours=6)
        elif hora == "09:00 - 12:00":
            sum_hour = timedelta(hours=9)
        elif hora == "12:00 - 15:00":
            sum_hour = timedelta(hours=12)
        elif hora == "15:00 - 18:00":
            sum_hour = timedelta(hours=15)
        elif hora == "18:00 - 21:00":
            sum_hour = timedelta(hours=18)
        elif hora == "21:00 - 00:00":
            sum_hour = timedelta(hours=21)

        today += sum_hour

        if (today - now).days >= 5:
            messages.warning(request, 'Selecione apenas até 5 dias.')
            today = now

    else:
        today = now

    location_str, location_id = local_str(local_id)

    # create or open db
    database()

    # TODO f1 xml = basex_actions.db_to_xml(db_name, location_str)
    # TODO dict_city = data_dict(xml)
    # TODO tparams getting info from dict_city
    tparams = {
        'title': f'Meteorologia - {today.day}/{today.month} - {today.hour}:00',
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
        'temp_inicio': today.hour,
        'temp_fim': today.hour + 3,
        'temp_dia': today.day
    }
    return render(request, 'forecast.html', tparams)


def api_call(city_id: int, key: str = '13bb9df7b5a4c16cbd2a2167bcfc7774'):  # d0279fea67692adea0e260e4cf86d072
    """

    :param city_id:
    :param key: api key
    :return:
    """

    # http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=13bb9df7b5a4c16cbd2a2167bcfc7774
    url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&units=metric&mode=xml&APPID={key}"

    request = requests.get(url=url)
    assert request.status_code == 200, f"Request error! Status {request.status_code}"

    xml = request.content.decode(request.encoding)

    # Create tmp.xml file
    with open(f"{edc_tp1.settings.XML_URL}tmp.xml", "w+") as xml_file:
        xml_file.write(xml)
    xml_root = etree.parse(f"{edc_tp1.settings.XML_URL}tmp.xml")
    xsd_root = etree.parse(f"{edc_tp1.settings.XML_URL}forecast.xsd")
    xsd = etree.XMLSchema(xsd_root)

    # Validate tmp.xml with xsd
    if xsd.validate(xml_root):
        return xml_root.getroot()
    else:
        print("Invalid XML file")


def database(name: str = "FiveDayForecast"):
    """

    :param name: name of db
    :return: if db does not exist, create and fill it with cities' weather info
            else, open db
    """
    try:
        session.execute(f"open {name}")
    except IOError:
        session.execute(f"create db {name}")

        db_root = etree.Element(name)
        for city in cities.values():
            root = api_call(city)
            db_root.append(root)  # Maybe use xupdate function instead
            # basex_actions.update_city(root, city)

        session.add(f"{name}.xml", etree.tostring(db_root).decode("utf-8"))


def data_dict(xml):
    """
    :param xml: xml with weather data of the city
    :return: dict with weather parameters (same format of tparams)
    """
    d = xmltodict.parse(xml)
    # TODO d is an OrderedDict, we may need to change to a simple dict
    return d


def get_local_id(city_name) -> tuple:
    """
    :param city_name: string with the name of the city
    :return: tuple of string and int, being the string the name of the city and int the id of the input city
    """
    city_id = cities.get(city_name, 2742611)
    if city_id == 2742611:
        return "Aveiro", city_id
    return city_name, city_id


def local_str(city_id) -> tuple:
    """
    :param city_id: int of the city
    :return: tuple of string and int, being the string the name of the city and int the id of the input city
    """

    for k, v in cities.items():
        if v == city_id:
            return k, v
    return "Aveiro", 2742611
