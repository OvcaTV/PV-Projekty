from config import connect


class ProductionService:
    def __init__(self):
        self.connection = connect()
        self.cursor = self.connection.cursor()

    def start_production(self, order_id: int, machine_ids: list[int]):
        """
        Spustí výrobu:
        - nastaví zakázku na Running
        - obsadí stroje
        - vytvoří vazby OrderMachine
        Vše v jedné transakci
        """

        try:
            self.connection.autocommit = False

            self.cursor.execute(
                """
                UPDATE ProductionOrder
                SET StatusId = 1, StartTime = GETDATE()
                WHERE OrderId = ?
                """,
                order_id
            )

            for machine_id in machine_ids:

                self.cursor.execute(
                    "SELECT IsOccupied FROM Machine WHERE MachineId = ?",
                    machine_id
                )
                occupied = self.cursor.fetchone()[0]

                if occupied:
                    raise Exception(f"Stroj {machine_id} je již obsazen")

                self.cursor.execute(
                    """
                    UPDATE Machine
                    SET IsOccupied = 1
                    WHERE MachineId = ?
                    """,
                    machine_id
                )

                self.cursor.execute(
                    """
                    INSERT INTO OrderMachine (OrderId, MachineId)
                    VALUES (?, ?)
                    """,
                    order_id, machine_id
                )

            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            raise e

        finally:
            self.connection.autocommit = True

    def close(self):
        self.cursor.close()
        self.connection.close()
