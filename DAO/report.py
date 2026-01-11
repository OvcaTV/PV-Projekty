from dao import DAO
from datetime import datetime


class ReportsDAO(DAO):

    def get_production_summary(self):
        self.cursor.execute(
            """
            SELECT os.Name AS Stav, COUNT(po.OrderId) AS PocetZakazek, SUM(po.Quantity) AS CelkoveMnozstvi, COUNT(DISTINCT po.ProductId) AS PocetRuznychProdukt
            FROM ProductionOrder po
            JOIN OrderStatus os ON po.StatusId = os.StatusId
            JOIN Product p ON po.ProductId = p.ProductId
            GROUP BY os.Name
            ORDER BY os.Name
            """
        )
        return self.cursor.fetchall()

    def get_machine_utilization(self):
        self.cursor.execute(
            """
            SELECT mt.Name AS TypStroje, COUNT(DISTINCT m.MachineId) AS CelkovyPocetStroju, SUM(CASE WHEN m.IsOccupied = 1 THEN 1 ELSE 0 END) AS ObsazeneStroje, COUNT(DISTINCT om.OrderId) AS PocetZakazek
            FROM Machine m
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            LEFT JOIN OrderMachine om ON m.MachineId = om.MachineId
            LEFT JOIN ProductionOrder po ON om.OrderId = po.OrderId AND po.StatusId = 1
            GROUP BY mt.Name
            ORDER BY mt.Name
            """
        )
        return self.cursor.fetchall()

    def get_product_statistics(self):
        self.cursor.execute(
            """
            SELECT p.Name AS Produkt, p.Weight AS Hmotnost, COUNT(po.OrderId) AS PocetZakazek, SUM(po.Quantity) AS CelkoveMnozstvi, SUM(po.Quantity * p.Weight) AS CelkovaHmotnost, AVG(CAST(po.Quantity AS FLOAT)) AS PrumerneMnozstvi
            FROM Product p
            LEFT JOIN ProductionOrder po ON p.ProductId = po.ProductId
            WHERE p.IsActive = 1
            GROUP BY p.ProductId, p.Name, p.Weight
            HAVING COUNT(po.OrderId) > 0
            ORDER BY CelkoveMnozstvi DESC
            """
        )
        return self.cursor.fetchall()

    def get_overall_statistics(self):
        self.cursor.execute(
            """
            SELECT 
                (SELECT COUNT(*) FROM ProductionOrder) AS CelkemZakazek,
                (SELECT COUNT(*) FROM ProductionOrder WHERE StatusId = 1) AS BeziciZakazky,
                (SELECT COUNT(*) FROM ProductionOrder WHERE StatusId = 2) AS DokonceneZakazky,
                (SELECT COUNT(*) FROM Product WHERE IsActive = 1) AS AktivnichProdukt,
                (SELECT COUNT(*) FROM Machine) AS CelkemStroju,
                (SELECT COUNT(*) FROM Machine WHERE IsOccupied = 1) AS ObsazenychStroju,
                (SELECT SUM(po.Quantity) FROM ProductionOrder po) AS CelkoveMnozstvi,
                (SELECT SUM(po.Quantity * p.Weight) 
                 FROM ProductionOrder po 
                 JOIN Product p ON po.ProductId = p.ProductId) AS CelkovaHmotnost
            """
        )
        return self.cursor.fetchone()

    def get_time_based_report(self):
        self.cursor.execute(
            """
            SELECT CAST(po.StartTime AS DATE) AS Datum, COUNT(po.OrderId) AS PocetZakazek, SUM(po.Quantity) AS CelkoveMnozstvi, COUNT(DISTINCT po.ProductId) AS PocetProdukt
            FROM ProductionOrder po
            WHERE po.StartTime IS NOT NULL
            GROUP BY CAST(po.StartTime AS DATE)
            ORDER BY Datum DESC
            """
        )
        return self.cursor.fetchall()

    def get_machine_workload(self):
        self.cursor.execute(
            """
            SELECT m.Name AS Stroj, mt.Name AS Typ, COUNT(DISTINCT om.OrderId) AS PocetZakazek, SUM(po.Quantity) AS CelkoveMnozstvi, m.IsOccupied AS Obsazeno
            FROM Machine m
            JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
            LEFT JOIN OrderMachine om ON m.MachineId = om.MachineId
            LEFT JOIN ProductionOrder po ON om.OrderId = po.OrderId
            GROUP BY m.MachineId, m.Name, mt.Name, m.IsOccupied
            ORDER BY PocetZakazek DESC, m.Name
            """
        )
        return self.cursor.fetchall()