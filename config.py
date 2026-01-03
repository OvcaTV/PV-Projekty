import configparser
import pyodbc


def connect():
    config = configparser.ConfigParser()
    config.read("config.ini")

    db = config["database"]

    connection_string = (
        f"DRIVER={{{db['driver']}}};"
        f"SERVER={db['server']};"
        f"DATABASE={db['database']};"
        f"Trusted_Connection={db['trusted_connection']};"
    )

    return pyodbc.connect(connection_string)
