from django.contrib import messages
from django.shortcuts import render
from datetime import datetime
from BaseXClient import BaseXClient
import xmltodict

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
    # TODO f1 get xml from db and location_id
    # TODO f2 function to get data structure from xml
    # TODO f3 tparams getting info from data_dict
    tparams = {
        'title': f'Meteorologia - {datetime.now().day}/{datetime.now().month}',
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


def db_to_xml(db_name: str, id: int):
    '''
    TODO f1
    :param db_name: name of database containing the data
    :param id: identification of the city
    :return: xml with city's weather info
    '''

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        xml = session.execute("xquery collection('{}')".format(db_name))
        # TODO filter here data with xquery, e.g. get only the city that was requested
    finally:
        session.close()

    return xml


def data_dict(xml):
    '''
    TODO f2: this function
    :param xml:
    :return: dict with weather parameters (same format of tparams)
    '''
    d = xmltodict.parse(xml)
    # TODO d is an OrderedDict, we may need to change to a simple dict
    return d


def local_id(str):
    '''
    TODO f4: translate using city.list.json
    :param str: string with the name of the city
    :return: int being the id of the input city
    '''
    return 2742611
