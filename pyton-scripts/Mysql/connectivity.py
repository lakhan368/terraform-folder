import mysql.connector
from mysql.connector import Error

def check_mysql_connection(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
            return True

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Example usage
host = 'your_host'
user = 'your_username'
password = 'your_password'
database = 'your_database'

if check_mysql_connection(host, user, password, database):
    print("Connection Successful!")
else:
    print("Connection Failed!")
    
    
    
import mysql.connector
from mysql.connector import Error

def list_tables(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")

            tables = cursor.fetchall()
            print(f"Tables in the database '{database}':")
            for table in tables:
                print(table[0])

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Example usage
host = 'your_host'
user = 'your_username'
password = 'your_password'
database = 'your_database'

list_tables(host, user, password, database)

import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Example usage
db_name = "your_db_name"
db_user = "your_db_user"
db_password = "your_db_password"
db_host = "your_db_host"
db_port = "your_db_port"

connection = create_connection(db_name, db_user, db_password, db_host, db_port)






from sqlalchemy import create_engine

def connect_to_postgres(db_user, db_password, db_host, db_port, db_name):
    try:
        # Create an engine instance
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

        # Connect to the PostgreSQL server
        connection = engine.connect()
        print("Connection to PostgreSQL DB successful")
        
        # Close the connection
        connection.close()
        print("PostgreSQL connection is closed")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Replace these with your actual database credentials
db_user = "your_db_user"
db_password = "your_db_password"
db_host = "your_db_host"
db_port = "your_db_port"
db_name = "your_db_name"

connect_to_postgres(db_user, db_password, db_host, db_port, db_name)