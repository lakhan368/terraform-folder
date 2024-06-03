import pymysql
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError



# Define your database connection details
db_endpoint = "my-mysql-db.cjqoyy8mmq6s.us-east-1.rds.amazonaws.com"
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
