from BaseXClient import BaseXClient
from lxml import etree
from datetime import timedelta
import xmltodict
from datetime import datetime, timedelta


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
    :return: xml with city's weather info: '<time...>...</time>'
    """

    assert date is datetime, "date should be datetime"

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        # TODO check if city is in db
        ...

        # if so Select city
        city_xml = session.execute("xquery collection('{}')//weatherdata[location/name='{}']"
                                   .format(db_name, city_name))
        # TODO if not, call from api and add to db
        ...

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

    # TODO Transform info to give only the necessary info (same as views.tparams)

    return info

