from dao import DAO


class MachineUsageVW(DAO):

    def get_all(self):
        self.cursor.execute(
            """
            SELECT
                MachineId,
                MachineName,
                MachineType,
                OrderId,
                ProductName,
                OrderStatus
            FROM MachineUsage
            """
        )
        return self.cursor.fetchall()

    def get_only_running(self):
        self.cursor.execute(
            """
            SELECT *
            FROM MachineUsage
            WHERE OrderStatus = 'Running'
            """
        )
        return self.cursor.fetchall()
