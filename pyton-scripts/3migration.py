import mysql.connector
import psycopg2

def fetch_mysql_data(host, mysql_user, mysql_password, mysql_database, table_name):
    """
    Fetch data from a MySQL table.

    Args:
    - host: MySQL host
    - mysql_user: MySQL username
    - mysql_password: MySQL password
    - mysql_database: MySQL database name
    - table_name: Name of the table to fetch data from

    Returns:
    - List of tuples containing the fetched data
    """
    try:
        # Establish connection to MySQL
        mysql_conn = mysql.connector.connect(
            host=host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = mysql_conn.cursor()

        # Fetch data from the MySQL table
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        # Close MySQL connection
        cursor.close()
        mysql_conn.close()

        return data
    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL: {e}")
        return None

def create_postgres_table(host, postgres_user, postgres_password, postgres_database, table_name, columns):
    """
    Create a table in PostgreSQL.

    Args:
    - host: PostgreSQL host
    - postgres_user: PostgreSQL username
    - postgres_password: PostgreSQL password
    - postgres_database: PostgreSQL database name
    - table_name: Name of the table to create
    - columns: List of column definitions in the format (column_name, data_type)

    Returns:
    - None
    """
    try:
        # Establish connection to PostgreSQL
        postgres_conn = psycopg2.connect(
            host=host,
            user=postgres_user,
            password=postgres_password,
            database=postgres_database
        )
        cursor = postgres_conn.cursor()

        # Construct CREATE TABLE query
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        query += ", ".join([f"{col[0]} {col[1]}" for col in columns])
        query += ")"

        # Execute CREATE TABLE query
        cursor.execute(query)
        postgres_conn.commit()

        # Close PostgreSQL connection
        cursor.close()
        postgres_conn.close()

        print(f"Table '{table_name}' created successfully in PostgreSQL.")
    except psycopg2.Error as e:
        print(f"Error creating table in PostgreSQL: {e}")

def insert_into_postgres(host, postgres_user, postgres_password, postgres_database, table_name, data):
    """
    Insert data into a PostgreSQL table.

    Args:
    - host: PostgreSQL host
    - postgres_user: PostgreSQL username
    - postgres_password: PostgreSQL password
    - postgres_database: PostgreSQL database name
    - table_name: Name of the table to insert data into
    - data: List of tuples containing data to insert

    Returns:
    - None
    """
    try:
        # Establish connection to PostgreSQL
        postgres_conn = psycopg2.connect(
            host=host,
            user=postgres_user,
            password=postgres_password,
            database=postgres_database
        )
        cursor = postgres_conn.cursor()

        # Construct INSERT INTO query
        query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(data[0]))})"

        # Execute INSERT INTO query
        cursor.executemany(query, data)
        postgres_conn.commit()

        # Close PostgreSQL connection
        cursor.close()
        postgres_conn.close()

        print(f"Data inserted into '{table_name}' in PostgreSQL successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")


# MySQL connection details
mysql_user = 'admin'
mysql_password = 'yourpassword'
mysql_host = "my-mysql-db.cjqoyy8mmq6s.us-east-1.rds.amazonaws.com"
mysql_database = 'mydatabase'
mysql_table = "employees"


postgres_user = 'test'
postgres_password = 'test1234'
postgres_host = 'mcapostgresdb.cjqoyy8mmq6s.us-east-1.rds.amazonaws.com'
postgres_database = 'postgressdb'
postgres_table = "employees"







# Fetch data from MySQL
data = fetch_mysql_data(mysql_host, mysql_user, mysql_password, mysql_database, mysql_table)

# Create PostgreSQL table with the same schema as MySQL table
# Assuming columns are fetched from MySQL INFORMATION_SCHEMA.COLUMNS
columns = [
    ("id", "INTEGER"),
    ("name", "VARCHAR(255)"),
    ("age", "INTEGER"),
    ("department", "VARCHAR(255)")
]
create_postgres_table(postgres_host, postgres_user, postgres_password, postgres_database, postgres_table, columns)

# Insert fetched data into PostgreSQL
if data:
    insert_into_postgres(postgres_host, postgres_user, postgres_password, postgres_database, postgres_table, data)







