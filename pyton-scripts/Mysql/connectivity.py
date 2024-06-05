#createtableimport pymysql
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Define your database connection details
db_endpoint = "my-mysql-db.c5kacoe2qvcb.us-east-1.rds.amazonaws.com"
db_port = 3306
db_name = "mydatabase"
db_username = "admin"
# Fetch the password from SSM Parameter Store
db_password = "yourpassword"

if db_password:
    try:
        # Connect to the RDS instance
        connection = pymysql.connect(
            host=db_endpoint,
            user=db_username,
            password=db_password,
            database=db_name,
            port=db_port
        )

        print("Connection to RDS successful!")

        # Create a cursor object
        cursor = connection.cursor()

        # SQL statement to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            department VARCHAR(50) NOT NULL
        )
        """

        # Execute the create table query
        cursor.execute(create_table_query)
        print("Table 'employees' created successfully!")

        # SQL statement to insert data into the table
        insert_data_query = """
        INSERT INTO employees (name, age, department)
        VALUES
            ('John Doe', 30, 'Engineering'),
            ('Jane Smith', 25, 'Marketing'),
            ('Sam Brown', 28, 'Human Resources')
        """

        # Execute the insert data query
        cursor.execute(insert_data_query)
        connection.commit()
        print("Data inserted successfully into 'employees' table!")

        # Fetch and display the data to confirm insertion
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
else:
    print("Failed to retrieve database password.")

#fetch table 
import mysql.connector
import pandas as pd

def get_mysql_table(host, user, password, database, table_name):
    """
    Retrieve a table from a MySQL database.

    Args:
    - host: MySQL host
    - user: MySQL username
    - password: MySQL password
    - database: MySQL database name
    - table_name: Name of the table to retrieve

    Returns:
    - pandas DataFrame containing the table data
    """
    # Establish connection to MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    try:
        # Query to select all rows from the table
        query = f"SELECT * FROM {table_name}"

        # Execute the query and fetch the results into a pandas DataFrame
        df = pd.read_sql(query, connection)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
user = 'admin'
password = 'yourpassword'
host = "my-mysql-db.c5kacoe2qvcb.us-east-1.rds.amazonaws.com"
database = 'mydatabase'
#ame = "employees"
table_name = "employees"




table_df = get_mysql_table(host, user, password, database, table_name)
if table_df is not None:
    print(f"Retrieved table '{table_name}' from MySQL database:")
    print(table_df.head())
else:
    print("Failed to retrieve table.")

#fetchalltables
[root@ip-172-31-30-190 ec2-user]# cat fetchalltables.py 
import mysql.connector

# Replace these values with your database connection details

user = 'admin'
password = 'yourpassword'
host = "my-mysql-db.c5kacoe2qvcb.us-east-1.rds.amazonaws.com"
dbname = 'mydatabase'
port = "3306"



try:
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connection successful")
    
    # Create a cursor object
    cur = conn.cursor()

    # Query to get all tables in the database
    cur.execute("SHOW TABLES;")
    tables = cur.fetchall()

    # Iterate through the tables and print their content
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")

        # Query to get all data from the table
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        # Get column names
        col_names = [i[0] for i in cur.description]
        print(" | ".join(col_names))
        
        # Print each row of the table
        for row in rows:
            print(" | ".join(str(cell) for cell in row))

    # Close the cursor and connection
    cur.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")

[root@ip-172-31-30-190 ec2-user]# cat postgresscheck.py 

import psycopg

# Replace these values with your database connection details
host = "mcapostgresdb.c5kacoe2qvcb.us-east-1.rds.amazonaws.com"
user = "test"
password = "test1234"
dbname = "postgressdb"
port = "5432"

try:
    # Connect to your PostgreSQL database
    conn = psycopg.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connection successful")
    
    # Create a cursor object
    cur = conn.cursor()

    # Execute a simple query
    cur.execute("SELECT version();")

    # Fetch the result
    db_version = cur.fetchone()
    print(f"Database version: {db_version}")

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")



