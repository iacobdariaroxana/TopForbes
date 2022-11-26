import psycopg2
from config import config_database


def get_connection():
    connection = None
    try:
        params = config_database()
        print('Connecting to the PostgreSQL database')
        connection = psycopg2.connect(**params)
    except psycopg2.DatabaseError as e:
        print(e)
    return connection


def close_connection(connection):
    if connection:
        connection.close()
        print('Database connection closed')
