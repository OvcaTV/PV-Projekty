from dao import DAO

class MachineDAO(DAO):

    def get_all(self):
        self.cursor.execute(
            """
            SELECT m.MachineId, m.Name, mt.Name, m.IsOccupied, m.IsActive
            FROM Machine m
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            ORDER BY m.MachineId
            """
        )
        return self.cursor.fetchall()

    def get_free_machines(self):
        self.cursor.execute(
            """
            SELECT m.MachineId, m.Name, mt.Name
            FROM Machine m
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            WHERE m.IsOccupied = 0 AND m.IsActive = 1
            """
        )
        return self.cursor.fetchall()

    def set_occupied(self, machine_id, occupied=True):
        self.cursor.execute(
            """
            UPDATE Machine
            SET IsOccupied = ?
            WHERE MachineId = ?
            """,
            int(occupied), machine_id
        )
        self.connect.commit()

    def get_machine_types(self):
        self.cursor.execute(
            """
            SELECT MachineTypeId, Name
            FROM MachineType
            ORDER BY Name
            """
        )
        return self.cursor.fetchall()

    def set_occupied(self, machine_id, occupied=True):
        self.cursor.execute(
            """
            UPDATE Machine
            SET IsOccupied = ?
            WHERE MachineId = ?
            """,
            int(occupied), machine_id
        )
        self.connect.commit()

    def set_active(self, machine_id, active=True):
        self.cursor.execute(
            """
            UPDATE Machine
            SET IsActive = ?
            WHERE MachineId = ?
            """,
            int(active), machine_id
        )
        self.connect.commit()

    def insert(self, name, machine_type_id):
        self.cursor.execute(
            "INSERT INTO Machine (Name, MachineTypeId, IsActive) VALUES (?, ?, 1)",
            name, machine_type_id
        )
        self.connect.commit()

    def delete(self, machine_id):
        self.cursor.execute(
            """
            DELETE FROM OrderMachine
            WHERE MachineId = ?
            """,
            machine_id
        )

        self.cursor.execute(
            """
            DELETE FROM Machine
            WHERE MachineId = ?
            """,
            machine_id
        )

        self.connect.commit()