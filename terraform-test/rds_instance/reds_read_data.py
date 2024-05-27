import pymysql
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Function to fetch the database password from AWS SSM Parameter Store


# Define your database connection details
db_endpoint = "terraform-20240526150319689600000001.cjgcesams7k4.us-east-1.rds.amazonaws.com"
db_port = 3306
db_name = "mydb"
db_username = "lakhan"

# Fetch the password from SSM Parameter Store
db_password = "lakhan361"

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

        # SQL statement to read data from the table
        read_data_query = "SELECT * FROM employees"

        # Execute the read data query
        cursor.execute(read_data_query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
else:
    print("Failed to retrieve database password.")
