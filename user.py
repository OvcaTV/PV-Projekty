from dao import DAO

class UserDAO(DAO):

    def authenticate(self, username, password):
        self.cursor.execute(
            """
            SELECT UserId, Username
            FROM Users
            WHERE Username = ? AND Password = ? AND IsActive = 1
            """,
            username, password
        )
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute(
            """
            SELECT UserId, Username, IsActive
            FROM Users
            ORDER BY Username
            """
        )
        return self.cursor.fetchall()

    def insert(self, username, password):
        self.cursor.execute(
            """
            INSERT INTO Users (Username, Password, IsActive)
            VALUES (?, ?, 1)
            """,
            username, password
        )
        self.connect.commit()

    def update_password(self, user_id, new_password):
        self.cursor.execute(
            """
            UPDATE Users
            SET Password = ?
            WHERE UserId = ?
            """,
            new_password, user_id
        )
        self.connect.commit()

    def set_active(self, user_id, active=True):
        self.cursor.execute(
            """
            UPDATE Users
            SET IsActive = ?
            WHERE UserId = ?
            """,
            int(active), user_id
        )
        self.connect.commit()

    def delete(self, user_id):
        self.cursor.execute(
            """
            DELETE FROM Users
            WHERE UserId = ?
            """,
            user_id
        )
        self.connect.commit()