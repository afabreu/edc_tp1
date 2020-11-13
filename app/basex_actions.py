from BaseXClient import BaseXClient


def db_to_xml(db_name: str, city_str: str):
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
