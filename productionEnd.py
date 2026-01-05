from config import connect


class ProductionEnd:
    def __init__(self):
        self.connect = connect()
        self.cursor = self.connect.cursor()

    def start_production(self, order_id: int, machine_ids: list[int]):
        try:
            self.connect.autocommit = False

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
                if self.cursor.fetchone()[0]:
                    raise Exception("Stroj uz je pouzivan")

                self.cursor.execute(
                    "UPDATE Machine SET IsOccupied = 1 WHERE MachineId = ?",
                    machine_id
                )

                self.cursor.execute(
                    "INSERT INTO OrderMachine (OrderId, MachineId) VALUES (?, ?)",
                    order_id, machine_id
                )

            self.connect.commit()

        except Exception:
            self.connect.rollback()
            raise

        finally:
            self.connect.autocommit = True

    def finish_production(self, order_id: int):
        try:
            self.connect.autocommit = False

            self.cursor.execute(
                """
                UPDATE ProductionOrder
                SET StatusId = 2, EndTime = GETDATE()
                WHERE OrderId = ?
                """,
                order_id
            )

            self.cursor.execute(
                "SELECT MachineId FROM OrderMachine WHERE OrderId = ?",
                order_id
            )
            machines = self.cursor.fetchall()

            for (machine_id,) in machines:
                self.cursor.execute(
                    "UPDATE Machine SET IsOccupied = 0 WHERE MachineId = ?",
                    machine_id
                )

            self.cursor.execute(
                "DELETE FROM OrderMachine WHERE OrderId = ?",
                order_id
            )

            self.connect.commit()

        except Exception:
            self.connect.rollback()
            raise

        finally:
            self.connect.autocommit = True

    def close(self):
        self.cursor.close()
        self.connect.close()
