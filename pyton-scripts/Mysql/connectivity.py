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