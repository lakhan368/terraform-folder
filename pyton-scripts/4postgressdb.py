import psycopg2

def connect_to_postgres(host, database, user, password):
    """
    Connect to a PostgreSQL database.

    Args:
    - host: PostgreSQL host
    - database: PostgreSQL database name
    - user: PostgreSQL username
    - password: PostgreSQL password

    Returns:
    - psycopg2 connection object
    """
    try:
        # Establish connection
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("Connected to PostgreSQL database successfully.")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def get_all_tables(connection):
    """
    Get a list of all tables in the PostgreSQL database.

    Args:
    - connection: psycopg2 connection object

    Returns:
    - List of table names
    """
    try:
        # Create a cursor
        cursor = connection.cursor()

        # Get all table names
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        # Fetch the result
        tables = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return [table[0] for table in tables]
    except psycopg2.Error as e:
        print(f"Error retrieving table names: {e}")
        return []

def get_table_data(connection, table_name):
    """
    Get the contents of a table in the PostgreSQL database.

    Args:
    - connection: psycopg2 connection object
    - table_name: Name of the table to retrieve data from

    Returns:
    - List of tuples representing the table rows
    """
    try:
        # Create a cursor
        cursor = connection.cursor()

        # Execute query to select all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch the result
        data = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return data
    except psycopg2.Error as e:
        print(f"Error retrieving data from table '{table_name}': {e}")
        return []

# Example usage
user = 'test'
password = 'test1234'
host = 'mcapostgresdb.cjqoyy8mmq6s.us-east-1.rds.amazonaws.com'
database = 'postgressdb'

# Connect to PostgreSQL
connection = connect_to_postgres(host, database, user, password)

if connection is not None:
    # Get all tables in the database
    tables = get_all_tables(connection)
    print("Tables in the database:")
    print(tables)

    # Retrieve and print contents of each table
    for table in tables:
        print(f"\nContents of table '{table}':")
        data = get_table_data(connection, table)
        if data:
            for row in data:
                print(row)
        else:
            print(f"No data found in table '{table}'.")

    # Close connection
    connection.close()
else:
    print("Failed to connect to PostgreSQL database.")



