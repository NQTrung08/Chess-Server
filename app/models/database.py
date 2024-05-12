import mysql.connector

from config import db_config


def get_database_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None
