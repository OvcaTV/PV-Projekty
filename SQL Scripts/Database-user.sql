CREATE LOGIN TestUser WITH PASSWORD = 'TestUser123!'; 
CREATE USER TestUser FOR LOGIN TestUser; 

ALTER ROLE db_datareader ADD MEMBER TestUser; 
ALTER ROLE db_datawriter ADD MEMBER TestUser; 
ALTER ROLE db_owner ADD MEMBER TestUser; 

GRANT SELECT, INSERT, UPDATE, DELETE on SCHEMA::dbo TO TestUser;

