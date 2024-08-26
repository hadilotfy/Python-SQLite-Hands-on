import sqlite3


def create_sample_db(db_file):
    """Creates a sample SQLite database and fills it with sample data.

    Args:
        db_file (str): Path to the SQLite database file.
    Returns:
        no returning.
        the function closes the program in case of an error.
    
    """
    conn = None 
    try:
        conn = sqlite3.connect(db_file)

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

        # Delete all rows to insert new data.
        cursor.execute('''
        DELETE FROM data;
        ''')

        # Insert data into the table.
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
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()
    finally:
        if conn :
            conn.close()


import pandas as pd
def read_from_database(db_file):
    """ Connect to DB and reads data into a Pandas DataFrame
    args
        db_file: string path of sqlite db file.
    returns
        Pandas DataFrame file with data retrieved from DB.
        Exits when error happens in the process.
    
    """
    conn = None 
    try:
        conn = sqlite3.connect(db_file)
        # df = pd.read_sql_query('SELECT id,name,email,zip_code,title FROM data', conn)
        df = pd.read_sql_query('SELECT * FROM data', conn)
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
    finally:
        if conn :
            conn.close()    
    return df 