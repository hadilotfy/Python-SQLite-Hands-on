"""
database module
---------------
Handle interactions with DB files from creating them , initializing 
with data and reading from them into Pandas.DataFrame objects.

"""


import sqlite3
import pandas as pd
from typing import Optional,Union,Iterable


import sqlite3
from typing import Optional

class etl_db_conn:
    def __init__(self, db_path: str):
        """
        Initialize the etl_db_conn class with the given database path.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path

        self.connection = None

    def __enter__(self):
        """
        Establish the database connection and return the connection object.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection when exiting the context.

        Args:
            exc_type (type): The type of exception raised, if any.
            exc_value (Exception): The exception instance, if any.
            traceback (traceback): The traceback object, if any.
        """
        if self.connection:
            self.connection.close()


def create_sample_db(db_file):
    """Creates a sample SQLite database and fills it with sample data.

    Args:
        db_file (str): Path to the SQLite database file.
    Returns:
        no returning.
    
    """
    
    try:
        with etl_db_conn(db_file) as conn:

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
                        , ('Samy' , 'Samy@yahoo.com' ,'789','IT')
                        , ('Hend' , 'Hend@hotmail.com' ,'123','HR')
                        , ('Amira', None ,None,'Backend Developer')
                        , ('Emad' , 'Emad@gmail.com' ,'789','Frontend Developer')
                        , ('Fathy', 'Fathy@hotmail.com','123','IT')
                        , ('Fahmy', 'Fahmy@hotmail.com','456','HR')
                        , ('Omar' , 'Omar@gmail.com' ,None,'Backend Developer')
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


def read_from_database(db_conn:etl_db_conn , chunksize:Optional[int]=None) -> Union[pd.DataFrame,Iterable[pd.DataFrame]]:
    """ Reads data from a DB Connection into a Pandas DataFrame
    args
        db_conn: db connection to read from.
    returns
        Pandas DataFrame file with data retrieved from DB.
        Exits when error happens in the process.
    """
    
    try:
        data = pd.read_sql_query('SELECT * FROM data', db_conn,chunksize=chunksize)

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
    return data

