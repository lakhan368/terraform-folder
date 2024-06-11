import mysql.connector
import os

def lambda_handler(event, context):
    # Database connection parameters from environment variables
    db_config = {
        'user': os.environ['DB_USERNAME'],
        'password': os.environ['DB_PASSWORD'],
        'host': os.environ['DB_HOST'],
        'database': os.environ['DB_NAME'],
        'port': os.environ.get('DB_PORT', 3306),
        'raise_on_warnings': True
    }
    
    try:
        # Attempt to connect to the database
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            return {
                'statusCode': 200,
                'body': 'Successfully connected to the database.'
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Failed to connect to the database.'
            }
    
    except mysql.connector.Error as err:
        return {
            'statusCode': 500,
            'body': f'Error connecting to database: {str(err)}'
        }
    
    finally:
        if connection.is_connected():
            connection.close()
