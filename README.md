# A hitchhiker's guide to this project's instalation  

## 0. Download the whole project into .zip under Code and Download ZIP. After downloading it, unzip it, then proceed to step 1.  
  <img width="390" height="295" alt="image" src="https://github.com/user-attachments/assets/a6e95ff5-98f3-48a5-8e1b-3623c92e206f" />

  
## 1. Create database in Microsoft SQL Server Management Studio  
You should start by creating database from scripts in SQL Scripts folder. There you should start with script DatabaseCreate, then continue with scripts Database-inserts, Database-user, Database-View1 and Database-View2.
In the end, you should end up with database diagram looking like this:  

<img width="972" height="900" alt="obrazek" src="https://github.com/user-attachments/assets/583cca0e-3155-42de-9bfe-30faad11aaa5" />

  
## 2. Open config.ini file
First you must change the server name in config.ini file to the server name of your Server Management Studio (it can be something like PCXXX with the XXX standing for numbers next to it or something simmilar to that)  

<img width="315" height="151" alt="obrazek" src="https://github.com/user-attachments/assets/51672a5a-490c-41bc-adef-a36815b67abc" />  



  
## 3. Running the project
1. Next you can continue by either running main.py file in command prompt or by opening and running this project in some Python IDE such as Pycharm
2. After running the project, you'll encounter login page. Don't be shy and register yourself. But i must warn you, that the password must be equal to or longer than 6 letters
3. You're inside and you can do whatever you want. Want to create new product? Create it in product. Want to create new Order? Select the product and amount of the product you want to create. Want to create new machine? You can create new machine in the machine tab. Want to start new order? Select the order you created in the combobox and then machine you want to use and its starts getting produced. Want to stop the order? Stop it. The fantasy's the only limit

Also if you want to use Windows authentication and be as admin you can just change the trusted connection to yes  
<img width="315" height="151" alt="obrazek" src="https://github.com/user-attachments/assets/66e993dd-bd33-46a5-9384-615b12acd918" />
