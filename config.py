import configparser
import pyodbc


def connect():
    config = configparser.ConfigParser()
    config.read("config.ini")

    db = config["database"]
    use_trusted = db.get('trusted_connection', 'no').lower() in ['yes', 'true', '1']

    if use_trusted:
        connection_string = (
            f"DRIVER={{{db['driver']}}};"
            f"SERVER={db['server']};"
            f"DATABASE={db['database']};"
            f"Trusted_Connection={db['trusted_connection']};"
    )
    else:
        connection_string = (
            f"DRIVER={{{db['driver']}}};"
            f"SERVER={db['server']};"
            f"DATABASE={db['database']};"
            f"UID={db['username']};"
            f"PWD={db['password']};"
        )

    return pyodbc.connect(connection_string)




