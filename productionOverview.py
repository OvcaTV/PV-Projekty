from dao import DAO


class ProductionOverviewViewDAO(DAO):

    def get_all(self):
        self.cursor.execute(
            """
            SELECT
                OrderId,
                ProductName,
                Quantity,
                Status,
                StartTime,
                EndTime
            FROM vw_ProductionOverview
            """
        )
        return self.cursor.fetchall()

    def get_by_status(self, status_name: str):
        self.cursor.execute(
            """
            SELECT
                OrderId,
                ProductName,
                Quantity,
                Status,
                StartTime,
                EndTime
            FROM vw_ProductionOverview
            WHERE Status = ?
            """,
            status_name
        )
        return self.cursor.fetchall()
