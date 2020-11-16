from BaseXClient import BaseXClient
from lxml import etree
import xmltodict
from datetime import datetime
import requests
import edc_tp1.settings


def db_to_xml(city_name: str,
              db_name: str = "FiveDaysForecast",
              date: datetime = datetime.now(),
              is_forecast: bool = False) -> dict:
    """
    TODO
    :param db_name: name of database containing the data
    :param city_name: name of the city
    :param date: day of requested weather info
    :param is_forecast: True if it is a forecast
    :return: dict with city's weather info
    """

    assert type(date) is datetime, "date should be datetime"

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:

        city_xml = session.execute("xquery collection('{}')//weatherdata[location/name='{}']"
                                   .format(db_name, city_name))
        if city_xml == "":
            add_city_to_db(city_name)

        # Parse xml to dict
        city_dict = xmltodict.parse(city_xml)

        # list with all nodes as dict
        times = city_dict['weatherdata']['forecast']['time']

        # info will be the correct time node
        info = {}

        # select date and time
        if is_forecast:
            for timestamp in times:
                f, t = timestamp['@from'], timestamp['@to']
                # select correct node based on data
                start = datetime.strptime(f.replace("T", " "), "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(t.replace("T", " "), "%Y-%m-%d %H:%M:%S")
                if start <= date < end:
                    info = timestamp
                    break
        else:
            info = times[0]

    finally:
        session.close()

    assert info != {}, "Info should not be empty: Date was not found"

    return info


def add_city_to_db(city, base_name: str = "FiveDayForecast"):

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    try:
        session.execute(f"open {base_name}")
    except IOError:
        session.execute(f"create db {base_name}")

    finally:
        db_root = etree.Element(base_name)
        root = api_call(city, to_string=False)
        # TODO delete next line and implement same action through xupdate
        db_root.append(root)

        session.add(f"{base_name}.xml", etree.tostring(db_root).decode("utf-8"))
        session.close()


def api_call(city_id: int, key: str = '13bb9df7b5a4c16cbd2a2167bcfc7774',
             to_string: bool = False, city_name: str = ""):  # d0279fea67692adea0e260e4cf86d072
    """

    :param city_id:
    :param key: api key
    :param to_string: if true, returns xml in string form. if not, in etree.Element root form
    :param city_name: name of city if needed ("" if not)
    :return:
    """

    # http://api.openweathermap.org/data/2.5/forecast?id=2742611&units=metric&mode=xml&APPID=13bb9df7b5a4c16cbd2a2167bcfc7774

    if city_name == "":
        url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&units=metric&mode=xml&APPID={key}"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},PT&APPID={key}&mode=xml&units=metric&lang=pt"

    request = requests.get(url=url)
    assert request.status_code == 200, f"Request error! Status {request.status_code}"

    xml = request.content.decode(request.encoding)

    if city_id == -1:
        xml_root = validate_current(xml)
    else:
        xml_root = validate_forecast(xml)

    if to_string:
        return xml
    else:
        return xml_root


def validate_forecast(xml: str) -> etree.Element:
    """

    :param xml:
    :return:
    """
    return validate(is_forecast=True, xml=xml)


def current_weather(city_name: str, key: str = '13bb9df7b5a4c16cbd2a2167bcfc7774',
                    to_string: bool = False):
    return api_call(city_id=-1, key=key, city_name=city_name, to_string=to_string)


def validate_current(xml: str) -> etree.Element:
    """

    :param xml:
    :return:
    """
    return validate(is_forecast=False, xml=xml)


def validate(is_forecast: bool, xml: str) -> etree.Element:
    """

    :param is_forecast:
    :param xml:
    :return:
    """
    fw = "weather"
    if is_forecast:
        fw = "forecast"

    # Create tmp.xml file
    with open(f"{edc_tp1.settings.XML_URL}tmp.xml", "w+") as xml_file:
        xml_file.write(xml)

    xml_name = f"{edc_tp1.settings.XML_URL}tmp.xml"
    xml_root = etree.parse(xml_name)

    xsd_name = f"{edc_tp1.settings.XML_URL}{fw}.xsd"
    xsd_root = etree.parse(xsd_name)

    xsd = etree.XMLSchema(xsd_root)

    # Validate tmp.xml with xsd
    if xsd.validate(xml_root):
        return xml_root.getroot()
    else:
        raise AssertionError(f"{xsd_name.split('/')[-1]} said {xml_name.split('/')[-1]} is invalid")
