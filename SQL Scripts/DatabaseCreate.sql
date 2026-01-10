create database PythonEvidence;
go

use PythonEvidence;
go;


CREATE TABLE OrderStatus (
    StatusId INT PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL
);

CREATE TABLE MachineType (
    MachineTypeId INT PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL
);

CREATE TABLE Product (
    ProductId INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Weight FLOAT NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1
);

CREATE TABLE Machine (
    MachineId INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    MachineTypeId INT NOT NULL,
    IsOccupied BIT NOT NULL DEFAULT 0,
	IsActive BIT NOT NULL DEFAULT 1
    FOREIGN KEY (MachineTypeId) REFERENCES MachineType(MachineTypeId)
);

CREATE TABLE ProductionOrder (
    OrderId INT IDENTITY(1,1) PRIMARY KEY,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    StatusId INT NOT NULL,
    StartTime DATETIME NULL,
    EndTime DATETIME NULL,
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId),
    FOREIGN KEY (StatusId) REFERENCES OrderStatus(StatusId)
);

CREATE TABLE OrderMachine (
    OrderId INT NOT NULL,
    MachineId INT NOT NULL,
    PRIMARY KEY (OrderId, MachineId),
    FOREIGN KEY (OrderId) REFERENCES ProductionOrder(OrderId),
    FOREIGN KEY (MachineId) REFERENCES Machine(MachineId)
);

CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Password NVARCHAR(255) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1
);