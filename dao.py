from config import get_connection

class DAO:
    def __init__(self):
        self.connect = get_connection()
        self.cursor = self.connect.cursor()

    def close(self):
        self.cursor.close()
        self.connect.close()