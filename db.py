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
def update_data(db_name, table_name, update_query, values):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f"UPDATE {table_name} SET {update_query}", values)
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


# print(retrieve_data('above.db', 'jewels')) ---> to retrieve all data


@app.route('/jewels', methods=['GET'])
def get_jewels():
    jewels = retrieve_data('above.db','jewels')
    return jsonify(jewels)


@app.route('/jewels', methods=['POST'])
def post_jewel():
    add_jewel = request.json
    insert_data('above.db', 'jewels', tuple(add_jewel.values()))
    return jsonify({"message": "Jewel added successfully"}), 201


@app.route('/jewels', methods=['PUT'])
def put_jewel():
    update_jewel = request.json
    update_query = ("category = ?, name = ?, size = ?, color = ?, material = ?, "
                    "quantity = ?, cost = ?, price = ? WHERE jewel_id = ?")
    values = (update_jewel['category'], update_jewel['name'], update_jewel['size'],
              update_jewel['color'], update_jewel['material'], update_jewel['quantity'],
              update_jewel['cost'], update_jewel['price'], update_jewel['jewel_id'])
    update_data('above.db', 'jewels', update_query, values)
    return jsonify({"message": "Jewel was successfully updated"}), 201


@app.route('/jewels/<jewel_id>', methods=['DELETE'])
def delete_jewel(jewel_id):
    delete_query = f"jewel_id = '{jewel_id}'"
    delete_data('above.db', 'jewels', delete_query)
    return jsonify({"message": "Jewel deleted successfully"}), 200


if __name__ == '__main__':
    create_database(DB_NAME)
    create_table(DB_NAME, 'jewels', 'jewel_id text, category text, name text, '
                                    'size text, color text, material text, quantity real, '
                                    'cost real, price REAL')
    app.run(debug=True)