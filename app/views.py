from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, timedelta
from app import basex_actions
from lxml import etree
from BaseXClient import BaseXClient
import json
import edc_tp1.settings
import requests

# URL to Weather XML:
# http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=d0279fea67692adea0e260e4cf86d072

# Create your views here.

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

# eg: {'Aveiro': 1, 'Lisboa': 2, ...}
cities = {}
all_pt_cities = {}

with open(edc_tp1.settings.TESTING_JSON) as f:
    json_data = json.loads(f.read())
    for jd in json_data:
        cities[jd['name']] = jd['id']

with open(edc_tp1.settings.CITIES_JSON) as f:
    json_data = json.loads(f.read())
    for jd in json_data:
        all_pt_cities[jd['name']] = jd['id']


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

    root_current = basex_actions.current_weather(location_str)
    xslt_file = etree.parse(f"{edc_tp1.settings.XML_URL}weather.xsl")
    transform = etree.XSLT(xslt_file)
    html = transform(root_current)

    context = {
        'title': f'Meteorologia - {datetime.now().day}/{datetime.now().month}',
        'year': datetime.now().year,
        'location': location_str,
        'location_id': location_id,
        'content': html
    }
    return render(request, 'index.html', context)


def forecast(request, local_id):
    now = datetime.now()  # Dia e Hora(com minutos, segundos, etc) atuais
    remove_min_sec = timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now -= remove_min_sec  # Dia e Hora(apenas hora) atuais
    hour_of_today = now.hour
    remove_hour = timedelta(hours=hour_of_today)
    submit_day = now - remove_hour  # Dia de hoje (sem horas)
    hour_of_today -= (hour_of_today % 3)  # Hora atual divisível por 3 anterior
    now = submit_day + timedelta(hours=hour_of_today)
    if 'inputDia' in request.POST and 'inputHora' in request.POST:
        dia = request.POST['inputDia']
        hora = request.POST['inputHora']

        if dia == "Amanhã":
            sum_day = 1
        elif dia == "Daqui a 2 dias":
            sum_day = 2
        elif dia == "Daqui a 3 dias":
            sum_day = 3
        elif dia == "Daqui a 4 dias":
            sum_day = 4
        elif dia == "Daqui a 5 dias":
            sum_day = 5
        else:
            sum_day = 0

        submit_day += timedelta(days=sum_day)

        if hora == "00:00 - 03:00":
            sum_hour = 0
        elif hora == "03:00 - 06:00":
            sum_hour = 3
        elif hora == "06:00 - 09:00":
            sum_hour = 6
        elif hora == "09:00 - 12:00":
            sum_hour = 9
        elif hora == "12:00 - 15:00":
            sum_hour = 12
        elif hora == "15:00 - 18:00":
            sum_hour = 15
        elif hora == "18:00 - 21:00":
            sum_hour = 18
        elif hora == "21:00 - 00:00":
            sum_hour = 21

        submit_day += timedelta(hours=sum_hour)

        difference_data = submit_day - now

        if difference_data.days >= 5 or difference_data.days < 0:
            messages.warning(request, 'Selecione apenas até 5 dias.')
            submit_day = now

    else:
        submit_day = now

    location_str, location_id = local_str(local_id)

    # create or open db
    database()

    query = f"""for $a in collection('FiveDayForecast')//weatherdata 
                for $b in $a/forecast/time 
                    where $a//name = "Aveiro" and $b/@from = "{submit_day.isoformat()}"
                    return $b"""
    query2 = session.query(query)
    xml_forecast = query2.execute()
    if xml_forecast == "":
        basex_actions.update_forecast(location_id)
    root_forecast = etree.XML(xml_forecast)

    xslt_file = etree.parse(f"{edc_tp1.settings.XML_URL}forecast.xsl")
    transform = etree.XSLT(xslt_file)
    html = transform(root_forecast)

    context = {
        'title': f'Meteorologia - {submit_day.day}/{submit_day.month} - {submit_day.hour}:00',
        'year': datetime.now().year,
        'location': f'{location_str}',
        'temp_inicio': submit_day.hour,
        'temp_fim': submit_day.hour + 3,
        'temp_dia': submit_day.day,
        'content': html
    }

    return render(request, 'forecast.html', context)


def news(request):
    rss = requests.get("http://www.ipma.pt/resources.www/rss/rss.news.ipma.xml")
    assert rss.status_code == 200, f"Request error! Status {rss.status_code}"
    # rss = rss.text
    rss = rss.content.decode(rss.encoding)
    rss = rss.replace('&A', '&amp;A')

    with open(f'{edc_tp1.settings.XML_URL}test.xml', 'w+', encoding="UTF-8") as file:
        file.write(rss)

    with open(f'{edc_tp1.settings.XML_URL}test.xml', 'r+') as file:
        xml = file.read()

    #    xml = etree.parse(f"{edc_tp1.settings.XML_URL}rss.news.ipma.xml")
    xml = etree.fromstring(xml)

    xsd_root = etree.parse(f"{edc_tp1.settings.XML_URL}rss.news.ipma.xsd")
    xsd = etree.XMLSchema(xsd_root)

    xsd.validate(xml)

    xslt_file = etree.parse(f"{edc_tp1.settings.XML_URL}rss.xsl")
    transform = etree.XSLT(xslt_file)
    html = transform(xml)

    context = {
        'year': datetime.now().year,
        'rss': html
    }
    return render(request, 'news.html', context)


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
    city_id = all_pt_cities.get(city_name, 2742611)
    if city_id == 2742611:
        return "Aveiro", city_id
    return city_name, city_id


def local_str(city_id) -> tuple:
    """
    :param city_id: int of the city
    :return: tuple of string and int, being the string the name of the city and int the id of the input city
    """

    for k, v in all_pt_cities.items():
        if v == city_id:
            return k, v
    return "Aveiro", 2742611
