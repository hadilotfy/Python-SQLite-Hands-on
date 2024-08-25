import sqlite3

def connect_to_db(path):
    try:
        conn = sqlite3.connect(path)
        # print("Database connection successful.")
        return conn
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
    except sqlite3.ProgrammingError as e:
        print(f"ProgrammingError: {e}")
    except sqlite3.InternalError as e:
        print(f"InternalError: {e}")
    except Exception as e:
        # Catch all other exceptions
        print(f"An unexpected error occurred: {e}")
    return None


def create_sample_db(db_file):
    """Creates a sample SQLite database."""
    conn = connect_to_db(db_file)
    if conn is None :
        print('Cannot connect to db, exiting...')
        exit(1)
    cursor = conn.cursor()

    # Create a sample table and insert some data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        zip_code TEXT,
        title TEXT
    )
    ''')

    # Delete all rows
    cursor.execute('''
    DELETE FROM data;
    ''')

    # Insert data into the table
    data_arr=[('Hadi' , 'Hadi@gmail.com' ,'123','Backend Developer')
                , ('Ramy' , 'Ramy@gmail.com' ,'456','Frontend Developer')
                , ('Samy' , 'Samy@gmail.com' ,'789','IT')
                , ('Hend' , 'Hend@gmail.com' ,'123','HR')
                , ('Amira', 'Amira@gmail.com','456','Backend Developer')
                , ('Emad' , 'Emad@gmail.com' ,'789','Frontend Developer')
                , ('Fathy', 'Fathy@gmail.com','123','IT')
                , ('Fahmy', 'Fahmy@gmail.com','456','HR')
                , ('Omar' , 'Omar@gmail.com' ,'789','Backend Developer')
                , ('Rana' , 'Rana@gmail.com' ,'123','Frontend Developer') ]
    cursor.executemany('''INSERT INTO data (name,email,zip_code,title)
                          VALUES (?, ?, ?, ?)''', data_arr )

    conn.commit()
    conn.close()

import pandas as pd
def read_from_database(db_file):
    conn = connect_to_db(db_file)
    if conn is None :
        print('Cannot connect to db, exiting...')
        exit(1)
    
    # df = pd.read_sql_query('SELECT id,name,email,zip_code,title FROM data', conn)
    df = pd.read_sql_query('SELECT * FROM data', conn)

    conn.close()  # Close the connection
    
    return df
