from config import connect

class DAO:
    def __init__(self):
        self.connect = connect()
        self.cursor = self.connect.cursor()

    def close(self):
        self.cursor.close()
        self.connect.close()