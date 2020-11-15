from BaseXClient import BaseXClient
from lxml import etree
from datetime import timedelta
import xmltodict


def db_to_xml(city_name: str,
              db_name: str = "FiveDaysForecast",
              sum_day: timedelta = timedelta(days=0),
              sum_hour: timedelta = timedelta(hours=0)) -> str:
    """
    TODO
    :param db_name: name of database containing the data
    :param city_name: identification of the city
    :param sum_day: days into the forecast
    :param sum_hour: hours into the forecast
    :return: xml with city's weather info: '<time...>...</time>'
    """

    is_forecast = False

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        xml = session.execute("xquery collection('{}')".format(db_name))
        # TODO filter data to get requested city's weather parameters
        #   select city
        #   select date and time
        ...
    finally:
        session.close()

    return xml


def update_db(bd_name: str, xml: str):
    """
    TODO maybe change the function's name to something more specific,
        if more xupdate functions are added
    :param bd_name: Name of the database
    :param xml: xml coming from the api
    :return: Updates the db
    """

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        # TODO the required update
        ...
    finally:
        session.close()


def update_city(root: etree.Element, city: str):
    """

    :param root: xml element
    :param city: city name
    :return: modifies database (xupdate)
    """
    xml = root_to_xml(root)
    ...


def root_to_xml(root: etree.Element) -> str:
    """

    :param root: root of xml
    :return: whole xml as string
    """
    ...
