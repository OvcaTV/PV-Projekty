from dao import DAO

class ProductionOrder(DAO):

    def get_all(self):
        self.cursor.execute(
            """
            SELECT
                po.OrderId,
                p.Name AS Product,
                po.Quantity,
                os.Name AS Status,
                po.StartTime,
                po.EndTime
            FROM ProductionOrder po
            JOIN Product p ON po.ProductId = p.ProductId
            JOIN OrderStatus os ON po.StatusId = os.StatusId
            """
        )
        return self.cursor.fetchall()

    def insert(self, product_id, quantity):
        self.cursor.execute(
            """
            INSERT INTO ProductionOrder (ProductId, Quantity, StatusId)
            VALUES (?, ?, 2)
            """,
            product_id, quantity
        )
        self.connect.commit()

    def delete(self, order_id):
        self.cursor.execute(
            """
            DELETE FROM OrderMachine
            WHERE OrderId = ?
            """,
            order_id
        )

        self.cursor.execute(
            """
            DELETE FROM ProductionOrder
            WHERE OrderId = ?
            """,
            order_id
        )

        self.connect.commit()
