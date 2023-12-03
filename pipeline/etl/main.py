"""Run the the full ETL pipeline."""
from os import environ, listdir
from shutil import move

from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection

from extract import create_driver, run_extract, setup
from transform import get_listing_data
from load import run_load

CITIES = ['london', 'bristol', 'manchester', 'birmingham']
FOLDER_PATHS = "{}/{}"


def db_connection() -> connection:
    """
    Establish a connection with the database.
    Returns a psycopg2 database connection object or None if connection fails.
    """
    try:
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_HOST"],
                       password=environ["DATABASE_PASSWORD"]
                       )
    except Exception as exc:
        raise DatabaseError("Error connecting to database.") from exc


def run_pipeline(conn):
    """Runs ETL pipeline."""
    for city in CITIES:
        print(f"processing {city}")
        setup(city)
        run_extract(city)
        path = FOLDER_PATHS.format(city, 'listing', '')
        webpage_path = FOLDER_PATHS.format(city, 'page', '')
        files = listdir(path)
        for file in files:
            try:
                listing_data = get_listing_data(path, file)
            except AttributeError as err:
                print(f"Error processing {file}: {err}")
                continue
            run_load(conn, file.strip('.html'), listing_data)
            move(f"{path}/{file}", f"archive/{path}/{file}")
        for page in listdir(webpage_path):
            move(f"{webpage_path}/{page}", f"archive/{webpage_path}/{page}")


if __name__ == "__main__":
    try:
        db_conn = db_connection()
        driver = create_driver()
        run_pipeline(db_conn)
    finally:
        db_conn.close()
        driver.quit()
