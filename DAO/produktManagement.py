from dao import DAO

class Product(DAO):

    def get_all(self):
        self.cursor.execute(
            """SELECT ProductId, Name, Weight, IsActive FROM Product
            WHERE IsActive = 1"""
        )
        return self.cursor.fetchall()

    def get_by_id(self, product_id):
        self.cursor.execute(
            "SELECT ProductId, Name, Weight, IsActive FROM Product WHERE ProductId = ?",
            product_id
        )
        return self.cursor.fetchone()

    def insert(self, name, weight):
        self.cursor.execute(
            "INSERT INTO Product (Name, Weight) VALUES (?, ?)",
            name, weight
        )
        self.connect.commit()

    def update(self, product_id, name, weight, is_active):
        self.cursor.execute(
            """
            UPDATE Product
            SET Name = ?, Weight = ?, IsActive = ?
            WHERE ProductId = ?
            """,
            name, weight, is_active, product_id
        )
        self.connect.commit()

    def delete(self, product_id):
        self.cursor.execute(
            "DELETE FROM Product WHERE ProductId = ?",
            product_id
        )
        self.connect.commit()