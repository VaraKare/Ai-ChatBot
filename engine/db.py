import csv
import sqlite3

connection = sqlite3.connect("database/edith.db")
# using cursor we can execuite quires
cursor= connection.cursor()

# query = 'CREATE TABLE IF NOT EXISTS  sys_command(' \
# 'id INTEGER PRIMARY KEY,' \
# 'name VARCHAR(100), ' \
# 'path VARCHAR(1000))'
# # Execute the query
# cursor.execute(query)

#sys application
# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)

#website
# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key," \
# " name VARCHAR(100), " \
# "url VARCHAR(1000))"
# cursor.execute(query)

#inserting values
# query = "INSERT INTO web_command VALUES (null,'google mail', 'https://mail.google.com/mail/u/1/#inbox')"
# cursor.execute(query)

#contacts

# query = "CREATE  TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY," \
# " name VARCHAR(200)," \
# " mobile_no VARCHAR(255), " \
# "email_id VARCHAR(255))"

desired_column_indices = [0,1]
with open('Contacts.csv','r',encoding="utf-8") as csv_file:
    csv_reader =csv.reader(csv_file)
    for row in csv_reader:
        selected_data = [row[i] for i in desired_column_indices]
        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null , ? , ?);''',tuple(selected_data) )
# cursor.execute("DELETE FROM contacts")
# Commit the changes and close the connection
connection.commit()
connection.close()

