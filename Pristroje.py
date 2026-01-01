from dao import DAO

class MachineDAO(DAO):

    def get_free_machines(self):
        self.cursor.execute(
            """
            SELECT m.MachineId, m.Name, mt.Name
            FROM Machine m
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            WHERE m.IsOccupied = 0
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
