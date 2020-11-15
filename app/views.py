from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, timedelta
from app import basex_actions
from lxml import etree
from BaseXClient import BaseXClient
import json
import edc_tp1.settings
import xmltodict

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
    weather_data = basex_actions.db_to_xml(location_str)
    tparams = {
        'title': f'Meteorologia - {datetime.now().day}/{datetime.now().month}',
        'year': datetime.now().year,
        'location': location_str,
        'location_id': location_id,
        'symbol': f"{weather_data['var']}: {weather_data['name']}",
        'precipitation': f"{weather_data['precipitation']['probability']*100}%",
        'windDirection': weather_data['windDirection']['name'],
        'windSpeed': f"{weather_data['mps']} {weather_data['unit']}",
        'temperature': f"{weather_data['value']} {weather_data['unit']}",
        'feels_like': f"{weather_data['value']} {weather_data['unit']}",
        'pressure': f"{weather_data['value']} {weather_data['unit']}",
        'humidity': f"{weather_data['value']} {weather_data['unit']}",
        'clouds': f"{weather_data['value']}, {weather_data['all']} {weather_data['unit']}",
        'visibility': weather_data['value'],
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

    # TODO f1 xml = basex_actions.db_to_xml(db_name, location_str, today)
    # TODO dict_city = data_dict(xml)
    # TODO tparams getting info from dict_city

    query = f"""for $a in collection('FiveDayForecast')//weatherdata 
                for $b in $a/forecast/time 
                    where $a//name = "Aveiro" and $b/@from = "{today.isoformat()}"
                    return $b"""
    query2 = session.query(query)
    res = query2.execute()
    root = etree.XML(res)

    xslt_file = etree.parse(f"{edc_tp1.settings.XML_URL}forecast.xsl")
    transform = etree.XSLT(xslt_file)
    html = transform(root)

    context = {
        'title': f'Meteorologia - {today.day}/{today.month} - {today.hour}:00',
        'year': datetime.now().year,
        'location': f'{location_str} - {location_id}',
        'symbol': "04d",
        'temp_inicio': today.hour,
        'temp_fim': today.hour + 3,
        'temp_dia': today.day,
        'content': html
    }

    return render(request, 'forecast.html', context)


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
            root = basex_actions.api_call(city)
            db_root.append(root)

        session.add(f"{name}.xml", etree.tostring(db_root).decode("utf-8"))


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
