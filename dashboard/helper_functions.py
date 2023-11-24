from os import environ

from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from psycopg2.sql import SQL
from dotenv import load_dotenv

from queries import top_requirements, all_requirements, listing_data


def db_connection() -> connection:
    """
    Establish a connection with the database.
    Returns a psycopg2 database connection object or None if connection fails.
    """
    try:
        load_dotenv()
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_HOST"],
                       password=environ["DATABASE_PASSWORD"]
                       )
    except DatabaseError as err:
        print(f"Error connecting to database: {err}")


def select_requirements():
    """Get all requirements from database"""
    return execute(all_requirements)


def select_top_requirements(n=10):
    """GET top N number of requirements from database"""
    return execute(SQL(top_requirements))


def select_listing_data():
    return execute(listing_data)


def execute(query):
    """Execute query blueprint"""
    try:
        conn = db_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
        return {"columns": columns, "rows": rows}
    except (AttributeError, DatabaseError) as err:
        print(f"Error querying database: {err}")
    finally:
        conn.close()
