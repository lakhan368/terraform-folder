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
host = "my-mysql-db.cjqoyy8mmq6s.us-east-1.rds.amazonaws.com"
database = 'mydatabase'
#ame = "employees"
table_name = "employees"




table_df = get_mysql_table(host, user, password, database, table_name)
if table_df is not None:
    print(f"Retrieved table '{table_name}' from MySQL database:")
    print(table_df.head())
else:
    print("Failed to retrieve table.")
