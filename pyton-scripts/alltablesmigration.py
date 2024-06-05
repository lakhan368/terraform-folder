import re
import mysql.connector
import psycopg2
import pandas as pd

def fetch_mysql_schema(mysql_host, mysql_user, mysql_password, mysql_db):
    mysql_conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

    schema = {}
    cursor = mysql_conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"SHOW CREATE TABLE {table_name}")
        create_table_statement = cursor.fetchone()[1]
        schema[table_name] = create_table_statement

    cursor.close()
    mysql_conn.close()

    return schema

def fetch_all_data(mysql_host, mysql_user, mysql_password, mysql_db):
    mysql_conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

    cursor = mysql_conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    all_data = {}

    for (table_name,) in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        all_data[table_name] = pd.DataFrame(rows, columns=columns)

    cursor.close()
    mysql_conn.close()

    return all_data

def convert_mysql_to_postgres(create_table_statement):
    # Replace backticks with double quotes for identifiers
    create_table_statement = create_table_statement.replace("`", "\"")
    
    # Replace int(11) or other int types with INTEGER
    create_table_statement = re.sub(r'\bint\(\d+\)\b', 'INTEGER', create_table_statement)
    
    # Replace TINYINT(1) with BOOLEAN
    create_table_statement = create_table_statement.replace("TINYINT(1)", "BOOLEAN")
    
    # Replace AUTO_INCREMENT with SERIAL and handle primary key
    create_table_statement = re.sub(r'\bINTEGER\s+NOT\s+NULL\s+AUTO_INCREMENT\b', 'SERIAL PRIMARY KEY', create_table_statement)
    create_table_statement = re.sub(r'\bINTEGER\s+AUTO_INCREMENT\b', 'SERIAL', create_table_statement)
    
    # Remove ENGINE, CHARSET, COLLATE, COMMENT, and other MySQL-specific table options
    create_table_statement = re.sub(r'ENGINE=\w+', '', create_table_statement)
    create_table_statement = re.sub(r'DEFAULT CHARSET=\w+', '', create_table_statement)
    create_table_statement = re.sub(r'COLLATE=\w+', '', create_table_statement)
    create_table_statement = re.sub(r'COMMENT=\'.*?\'', '', create_table_statement)
    
    # Replace double with DOUBLE PRECISION
    create_table_statement = create_table_statement.replace("double", "DOUBLE PRECISION")
    
    # PostgreSQL does not support unsigned, remove it
    create_table_statement = create_table_statement.replace("unsigned", "")
    
    # Remove any trailing commas before closing parentheses
    create_table_statement = re.sub(r',\s*\)', ')', create_table_statement)
    
    # Remove any residual =N assignments
    create_table_statement = re.sub(r'\s*=\s*\d+', '', create_table_statement)
    
    # Clean up any leftover MySQL specific syntax
    create_table_statement = create_table_statement.replace("AUTO_INCREMENT", "")
    
    return create_table_statement.strip()

def create_tables_in_postgres(postgres_host, postgres_user, postgres_password, postgres_db, schema):
    postgres_conn = psycopg2.connect(
        host=postgres_host,
        user=postgres_user,
        password=postgres_password,
        database=postgres_db
    )

    cursor = postgres_conn.cursor()

    for table_name, create_table_statement in schema.items():
        postgres_create_statement = convert_mysql_to_postgres(create_table_statement)
        try:
            cursor.execute(f"DROP TABLE IF EXISTS \"{table_name}\" CASCADE")
            cursor.execute(postgres_create_statement)
            print(f"Table {table_name} created successfully in PostgreSQL.")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")

    cursor.close()
    postgres_conn.commit()
    postgres_conn.close()

def insert_data_into_postgres(postgres_host, postgres_user, postgres_password, postgres_db, all_data):
    postgres_conn = psycopg2.connect(
        host=postgres_host,
        user=postgres_user,
        password=postgres_password,
        database=postgres_db
    )
    
    cursor = postgres_conn.cursor()
    
    for table_name, df in all_data.items():
        for index, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO \"{table_name}\" ({columns}) VALUES ({values})"
            cursor.execute(insert_query, tuple(row))
    
    cursor.close()
    postgres_conn.commit()
    postgres_conn.close()

# Example usage
# Example usage
mysql_user = 'admin'
mysql_password = 'yourpassword'
mysql_host = "my-mysql-db.cfocgm448lg6.us-east-1.rds.amazonaws.com"
mysql_db = 'mydatabase'


postgres_user = 'test'
postgres_password = 'test1234'
postgres_host = 'mcapostgresdb.cfocgm448lg6.us-east-1.rds.amazonaws.com'
postgres_db = 'postgressdb'

# Fetch MySQL schema and data
mysql_schema = fetch_mysql_schema(mysql_host, mysql_user, mysql_password, mysql_db)
all_data = fetch_all_data(mysql_host, mysql_user, mysql_password, mysql_db)

# Create tables in PostgreSQL
create_tables_in_postgres(postgres_host, postgres_user, postgres_password, postgres_db, mysql_schema)

# Insert data into PostgreSQL
insert_data_into_postgres(postgres_host, postgres_user, postgres_password, postgres_db, all_data)



fetch all tables
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

    # Fetch all table names
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cur.fetchall()

    # Loop through each table and fetch its content
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")

delete table
import psycopg

# Replace these values with your database connection details
host = "mcapostgresdb.c5kacoe2qvcb.us-east-1.rds.amazonaws.com"
user = "test"
password = "test1234"
dbname = "postgressdb"
port = "5432"

table_name_to_delete = "employees"

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

    # Execute a query to delete the table
    cur.execute(f"DROP TABLE IF EXISTS {table_name_to_delete};")
    print(f"Table '{table_name_to_delete}' deleted successfully.")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")





