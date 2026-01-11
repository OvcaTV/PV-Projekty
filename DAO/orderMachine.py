from dao import DAO


class OrderMachineDAO(DAO):

    def add_machine_to_order(self, order_id: int, machine_id: int):
        self.cursor.execute(
            """
            INSERT INTO OrderMachine (OrderId, MachineId)
            VALUES (?, ?)
            """,
            order_id, machine_id
        )
        self.conn.commit()

    def remove_machine_from_order(self, order_id: int, machine_id: int):
        self.cursor.execute(
            """
            DELETE FROM OrderMachine
            WHERE OrderId = ? AND MachineId = ?
            """,
            order_id, machine_id
        )
        self.conn.commit()

    def get_machines_for_order(self, order_id: int):
        self.cursor.execute(
            """
            SELECT m.MachineId, m.Name, mt.Name AS MachineType
            FROM OrderMachine om
            JOIN Machine m ON om.MachineId = m.MachineId
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            WHERE om.OrderId = ?
            """,
            order_id
        )
        return self.cursor.fetchall()

    def get_orders_for_machine(self, machine_id: int):
        self.cursor.execute(
            """
            SELECT po.OrderId,p.Name AS Product,po.Quantity
            FROM OrderMachine om
            JOIN ProductionOrder po ON om.OrderId = po.OrderId
            JOIN Product p ON po.ProductId = p.ProductId
            WHERE om.MachineId = ?
            """,
            machine_id
        )
        return self.cursor.fetchall()
