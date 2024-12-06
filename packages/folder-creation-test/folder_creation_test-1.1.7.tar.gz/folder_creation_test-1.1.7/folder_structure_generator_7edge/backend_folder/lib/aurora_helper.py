import psycopg2
import os

def get_db_connection():
    """
    The function `get_db_connection` establishes a connection to a PostgreSQL database using environment
    variables for the connection details.
    :return: The function `get_db_connection` returns a connection object to a PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host = os.environ['RDS_CLUSTER_HOST'],
            port = 5432,
            user = os.environ['RDS_CLUSTER_USERNAME'],
            password = os.environ['RDS_CLUSTER_PASSWORD'],
            database = os.environ['RDS_DATABASE_NAME'],
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        raise

def close_connection(connection, cursor):
    """Close the cursor and connection."""
    if cursor:
        cursor.close()
    if connection:
        connection.close()