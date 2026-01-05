# A hitchhiker's guide to this project's instalation  
  
## 1. Create database in Microsoft SQL Server Management Studio  
You should start by creating database from files in SQL Scripts folder. There you should start with script DatabaseCreate, then script Database-inserts, then Database-user, Database-View1 and finally Database-View2.
In the end, you should end up with database diagram looking like this:  

<img width="972" height="900" alt="obrazek" src="https://github.com/user-attachments/assets/583cca0e-3155-42de-9bfe-30faad11aaa5" />

  
## 2. Open project in Python IDE like Pycharm
Next you should continue by opening this project in IDE such as Pycharm

  
## 3. Running the project
1. First you must change the server name in config.ini file to the server name of your Server Management Studio  
<img width="315" height="151" alt="obrazek" src="https://github.com/user-attachments/assets/51672a5a-490c-41bc-adef-a36815b67abc" />  

2. After running the project, you'll encounter login page. Don't be shy and register yourself. But i must warn you, that the password must be longer than 6 letters
3. You're inside and you can do whatever you want. Want to create new product? Create it in product. Want to create new Order? Select the product and amount of the product you want to create. Want to create new machine? You can create new machine in the machine tab. Want to start new order? Select the order you created in the combobox and then machine you want to use and its starts getting produced. Want to stop the order? Stop it. The fantasy's the only limit

