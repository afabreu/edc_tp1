from BaseXClient import BaseXClient
from lxml import etree


def db_to_xml(db_name: str, city_str: str) -> str:
    """
    TODO f1
    :param db_name: name of database containing the data
    :param city_str: identification of the city
    :return: xml with city's weather info
    """

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        xml = session.execute("xquery collection('{}')".format(db_name))
        # TODO filter data to get requested city's weather parameters
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
