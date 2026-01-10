use PythonEvidence;
go;


CREATE view MachineUsage
AS
SELECT m.MachineId, m.Name AS MachineName, mt.Name AS MachineType, po.OrderId, p.Name AS ProductName, os.Name AS OrderStatus
FROM OrderMachine om
JOIN Machine m ON om.MachineId = m.MachineId
JOIN MachineType mt ON m.MachineTypeId = mt.MachineTypeId
JOIN ProductionOrder po ON om.OrderId = po.OrderId
JOIN Product p ON po.ProductId = p.ProductId
JOIN OrderStatus os ON po.StatusId = os.StatusId;