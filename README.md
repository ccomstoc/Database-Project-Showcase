In 2021, we were tasked to create a normalized SQL database with at least 5 tables. 
We then had to provide a list of functional dependencies, confirm it was in Boyce Cod 
normal form, draw up an ER diagram, and write a list of challenging queries for the database.

Now, in 2024, I have revisited this project. In an effort to better present it, I have created 
a GUI Python application using the PyQt5 and SQLite libraries. This application allows the user 
to browse all the tables we created, query the database, and run any of our premade queries easily.

The left pane is for viewing the tables in a pop out window, the middle pane is for browsing 
and running premade queries, and the right pane is for viewing the results of any query. 
All intended data is stored in the folder [defaultTables](defaultTables). Any table modification can be 
reverted by pressing the reset tables button. 

The pop out windows are defined respectively in [queryDialog.py](queryDialog.py) and [tableDialog.py](tableDialog.py). All the 
database interaction is handled by the database manager object defined in [databaseManager.py](databaseManager.py). 
The main app is defined in [app.py](app.py). Please note this project is dependent on PyQt5.
