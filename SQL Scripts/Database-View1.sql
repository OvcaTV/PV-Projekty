use PythonEvidence;
go;


CREATE VIEW ProductionOverview
AS
SELECT
    po.OrderId,
    p.Name AS ProductName,
    po.Quantity,
    os.Name AS Status,
    po.StartTime,
    po.EndTime
FROM ProductionOrder po
JOIN Product p ON po.ProductId = p.ProductId
JOIN OrderStatus os ON po.StatusId = os.StatusId;