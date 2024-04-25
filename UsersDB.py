import sqlite3
connection = sqlite3.connect("users.db")
print("Database opened successfully")
cursor = connection.cursor()
connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT , email TEXT, gender TEXT, contact TEXT, dob date, Enrollment_no TEXT , profile_pic BLOB)")
print("Table created successfully")
connection.close()   
