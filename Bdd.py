import sqlite3, json

def create_table(database, table, input_table:bool=False):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if input_table:
        sql_queries = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER PRIMARY KEY,
                LINK_A TEXT,
                LINK_B TEXT,
                WEIGHT INTEGER
            )
        """
    else:
        sql_queries = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER PRIMARY KEY ,
                TIME INTEGER,
                JSON TEXT,
                NODE INTEGER
            )
        """
    cursor.execute(sql_queries)

    conn.commit()
    conn.close()

def read_table(database: str, table: str):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    sql_query = f"SELECT * from {table}"
    cursor.execute(sql_query)

    rows = cursor.fetchall()  # Fetch all rows instead of just one row

    cursor.close()
    connection.close()

    return rows

def insert_data(database, table, time_val, json_val, node_val, input_table=False):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if input_table:
      cursor.execute(f"""
            INSERT INTO {table} (LINK_A, LINK_B, WEIGHT)
            VALUES (?, ?, ?)
        """, (time_val, json_val, node_val))
    else:
        cursor.execute(f"""
            INSERT INTO {table} (TIME, JSON, NODE)
            VALUES (?, ?, ?)
        """, (time_val, json_val, node_val))
        
    conn.commit()
    conn.close()

def update_data(database, table, id_val, time_val, json_val, node_val):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE {table}
        SET TIME = ?,
            JSON = ?,
            NODE = ?
        WHERE ID = ?
    """, (time_val, json_val, node_val, id_val))

    conn.commit()
    conn.close()

def test_update_data(database, table, id_val, time_val, json_val, node_val):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE {table}
        SET LINK_A = ?,
            LINK_B = ?,
            WEIGHT = ?
        WHERE ID = ?
    """, (time_val, json_val, node_val, id_val))

    conn.commit()
    conn.close()

def create_output_table(database, table):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    sql_query = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            ID INTEGER PRIMARY KEY,
            TIME INTEGER,
            JSON TEXT,
            NODE INTEGER
        )
    """
    cursor.execute(sql_query)

    conn.commit()
    conn.close()

def get_existing_data(database, table, json_val):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table} WHERE JSON = ?", (json_val,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "ID": row[0],
            "TIME": row[1],
            "JSON": row[2],
            "NODE": row[3]
        }
    else:
        return None

if __name__ == "__main__":
    with open("config.json","r",encoding="utf-8") as config_file:
        CONFIGURATION = json.loads(config_file.read())
        
    DATABASE = CONFIGURATION.get("database")
    TABLE = CONFIGURATION.get("table")

    DATABASE_OUTPUT = CONFIGURATION.get("database_output")
    TABLE_OUTPUT = CONFIGURATION.get("table_output")


    #create_table(DATABASE, TABLE, True)
    test_update_data(DATABASE, TABLE, 1, "A", "B", 2)
    """
    #insert_data(DATABASE, TABLE, 2, "B", "E",1,True)
    insert_data(DATABASE, TABLE, 3, "E", "C",4,True)
    insert_data(DATABASE, TABLE, 4, "C", "D",3,True)
    insert_data(DATABASE, TABLE, 5, "D", "A",3,True)
    insert_data(DATABASE, TABLE, 6, "E", "G",1,True)
    insert_data(DATABASE, TABLE, 7, "C", "G",3,True)
    insert_data(DATABASE, TABLE, 8, "G", "H",4,True)
    insert_data(DATABASE, TABLE, 9, "C", "H",9,True)
    insert_data(DATABASE, TABLE, 10, "C", "F",3,True)
    insert_data(DATABASE, TABLE, 11, "D", "F",5,True)
    """
