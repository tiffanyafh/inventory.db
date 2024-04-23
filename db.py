from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'above.db'

con = sqlite3.connect('above.db')
cur = con.cursor()


# Function to create a new SQLite database
def create_database(db_name):
    con = sqlite3.connect(db_name)
    con.close()


# Function to create a new table in the database
def create_table(db_name, table_name, columns):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    con.commit()
    con.close()


# Function to insert data into a table
def insert_data(db_name, table_name, data):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table_name} VALUES {data}")
    con.commit()
    con.close()


# Function to retrieve data from a table
def retrieve_data(db_name, table_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    con.close()
    return rows


# Function to update data in a table
def update_data(db_name, table_name, update_query):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"UPDATE {table_name} SET {update_query}")
    con.commit()
    con.close()
# update_query = "category = 'boob' WHERE jewel_id = 1"
# update_data('above.db', 'jewels', update_query)


# Function to delete data from a table
def delete_data(db_name, table_name, delete_query):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE {delete_query}")
    con.commit()
    con.close()


# Function to delete a table from the database
def delete_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    con.commit()
    con.close()


# Function to delete the entire database
def delete_database(db_name):
    import os
    if os.path.exists(db_name):
        os.unlink(db_name)
        print(f"The database file '{db_name}' has been deleted.")
    else:
        print(f"The database file '{db_name}' does not exist.")


print(retrieve_data('above.db', 'jewels'))


@app.route('/jewels', methods=['GET'])
def get_jewels():
    jewels = retrieve_data('above.db','jewels')
    return jsonify(jewels)


@app.route('/jewels', methods=['POST'])
def add_jewel():
    new_jewel = request.json
    insert_data('above.db', 'jewels', tuple(new_jewel.values()))
    return jsonify({"message": "Jewel added successfully"}), 201


if __name__ == '__main__':
    create_database(DB_NAME)
    create_table(DB_NAME, 'jewels', 'name TEXT, category TEXT, price REAL')
    app.run(debug=True)