import psycopg2
from config import config_database


def get_youngest(n):
    connection = None
    try:
        connection = psycopg2.connect(**config_database())
        cursor = connection.cursor()

        query = f"select name, age from billionaires where age is not null order by age fetch first {n} rows only"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        return results
    except psycopg2.DatabaseError as e:
        print(e)
    finally:
        if connection:
            connection.close()


def get_citizenship(citizenship):
    connection = None
    try:
        connection = psycopg2.connect(**config_database())
        cursor = connection.cursor()

        query = f"select count(*) from billionaires where country_of_citizenship='{citizenship}'"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return {citizenship: {"Yes": count, "No": (200 - count)}}
    except psycopg2.DatabaseError as e:
        print(e)
    finally:
        if connection:
            connection.close()


def get_highest_score(n):
    connection = None
    try:
        connection = psycopg2.connect(**config_database())
        cursor = connection.cursor()

        query = f"select name, net_worth from billionaires order by net_worth desc fetch first {n} rows only"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        return results
    except psycopg2.DatabaseError as e:
        print(e)
    finally:
        if connection:
            connection.close()

