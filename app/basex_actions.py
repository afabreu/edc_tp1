from BaseXClient import BaseXClient
from lxml import etree
import xmltodict
from datetime import datetime
import requests
import edc_tp1.settings


def db_to_xml(city_id: int,
              db_name: str = "FiveDaysForecast",
              date: datetime = datetime.now(),
              is_forecast: bool = False) -> dict:
    """
    :param db_name: name of database containing the data
    :param city_id: name of the city
    :param date: day of requested weather info
    :param is_forecast: True if it is a forecast
    :return: dict with city's weather info
    """

    assert type(date) is datetime, "date should be datetime"

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:

        city_xml = session.execute("xquery collection('{}')//weatherdata[location/name='{}']"
                                   .format(db_name, city_id))
        if city_xml == "":
            add_city_to_db(city_id)

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

                #
                if is_in_range(f, date, t):
                    info = timestamp
                    break
        else:
            info = times[0]

    finally:
        session.close()

    assert info != {}, "Info should not be empty: Date was not found"

    return info


def is_in_range(start: str, date_t: datetime, end: str) -> int:
    """

    :param date_t: datetime to evaluate
    :param start: left side of interval
    :param end: right side of interval
    :return: True if date_T is in interval or equals start, False otherwise
    """

    # TODO check if start/end format is correct
    ...
    # select correct node based on data
    start = datetime.strptime(start.replace("T", " "), "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end.replace("T", " "), "%Y-%m-%d %H:%M:%S")

    if start <= date_t < end:
        return 0
    elif start > date_t:
        return -1
    elif date_t >= end:
        return 1
    raise AssertionError("This was not supposed to happen")


def add_city_to_db(city: int, base_name: str = "FiveDayForecast"):
    """

    :param city: city id number
    :param base_name: database name (forecast as default)
    :return: Adds the city do the database
    """

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    try:
        session.execute(f"open {base_name}")
    except IOError:
        session.execute(f"create db {base_name}")
    finally:
        xml = api_call(city, to_string=True, remove_header=True)
        query = "xquery insert node {} as last into <{}>".format(xml, base_name)
        session.execute(query)

        session.close()


def update_forecast(city_name: str, city_id: int):
    """

    :param city_id:
    :param city_name: id of the city
    :return: update <time> nodes from the future (delete them and insert new ones from api)
    """

    # Call forecast data from api
    xml = api_call(city_id=city_id, to_string=True, remove_header=True)

    # Get the forecast node in str from the xml above
    xml_forecast = get_forecast_node(city_name, xml)

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        # Open forecast db
        session.execute(f"open FiveDayForecast")

        # Check if city is on db
        xq = "xquery collection('FiveDayForecast')//weatherdata[location/name='{}']"
        city_in_db = session.execute(xq).format(city_name) != ""
        if not city_in_db:
            add_city_to_db(city_id)

        # Delete forecast node
        session.execute("xquery delete node collection('FiveDayForecast')//weatherdata[location/name='{}']/forecast"
                        .format(city_name))

        # Insert new forecast node
        query = "xquery insert node {} as last into collection('FiveDayForecast')//weatherdata[location/name='{}']/forecast".\
            format(xml_forecast, city_name)
        session.execute(query)

    finally:
        session.close()


def xml_slice_by_datetime(date_time: datetime, xml: str, direction: str, inclusive: bool) -> list:
    """
    :param inclusive: include node with current datetime
    :param xml:
    :param date_time: datetime in which evaluations will be based on
    :param direction: if "after" give <time> nodes after the one with the given datetime
    :return: list of node strings
    """
    nodes_list = split_time_nodes(xml=xml)
    # Add list with nodes from past and nodes from future, respectively
    nodes_after = nodes_before = list()

    # Checking if nodes_list is a list of strings
    check = [type(node) is str for node in nodes_list]
    check = all(check) and type(check) is list
    assert check, f"Incorrect data type"

    # Checking there is only two possible directions
    assert direction in ['after', 'before']

    for time in nodes_list:

        # Check if this node is from past or future
        d = xmltodict.parse(time)
        verify = is_in_range(d['@from'], time, d['@to'])

        # Some verification of node syntax
        keys = ['time', 'symbol', 'precipitation', 'windDirection',
                'windSpeed', 'temperature', 'feels_like',
                'pressure', 'humidity', 'clouds', 'visibility']
        assert d.keys() in [keys[0]], f"Error in node validation: {d.keys()}"
        assert d[keys[0]].keys() in [keys[1:]], f"Error in node validation: {d[keys[0]].keys()}"

        # Add to proper list based on last verification
        if verify == -1:
            # In case its from future
            nodes_after.append(time)
        elif verify:
            # In case its from past
            nodes_before.append(time)
        else:
            # In case it's present time
            if inclusive:
                # Needs to be inclusive
                nodes_before.append(time)
                nodes_after.append(time)

    if direction == 'after':
        return nodes_after
    return nodes_before


def split_time_nodes(xml: str) -> list:
    """

    :param xml:
    :return:
    """

    # Take off \n
    xml = xml.replace('\n', '')

    # splitting collection to individuals
    split = [f"{time_node}</time>" for time_node in xml.split("</time>")]

    return split


def get_forecast_node(city_name: str, xml: str) -> str:
    """

    :param xml:
    :param city_name:
    :return:
    """

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    try:
        session.execute("create db database")

        session.add("HeadNode", xml)

        # Assert there is one only <weatherdata> node
        a = session.execute("xquery collection('database')//weatherdata")
        b = session.execute("xquery collection('database')/weatherdata")
        assert a == b

        # Execute query and save in xml

        query = """let $a:=collection('database')//weatherdata/forecast//time
                    return $a""".format(city_name)
        query2 = session.query(querytxt=query)
        xml_ = query2.execute()

        # Check var
        assert xml_ != "", "Error: xml_ var is empty"

        session.execute("drop db database")

    finally:
        session.close()

    return xml_


def api_call(city_id: int, key: str = '13bb9df7b5a4c16cbd2a2167bcfc7774',
             to_string: bool = False, city_name: str = "",
             remove_header: bool = False, current: bool = False):  # d0279fea67692adea0e260e4cf86d072
    """

    :param current:
    :param remove_header: remove xml header (redundant if to_string is False)
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

    if current:
        # Current xml data type
        xml_root = validate_current(xml)
    else:
        # Forecast xml data type
        xml_root = validate_forecast(xml)

    if to_string:
        if remove_header:
            return xml.split('\n')[-1]
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
    return api_call(city_id=-1, key=key, city_name=city_name, to_string=to_string, current=True)


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
