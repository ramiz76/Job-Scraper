"""Run the the full ETL pipeline."""
from datetime import datetime
from os import environ, listdir, makedirs

from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
import spacy

from extract import create_driver, run_extract
from transform import get_listing_data
from load import run_load

DATE = datetime.now().strftime("%y_%m_%d")
FULL_LISTING_URL = "https://www.totaljobs.com/{}"
ALL_LISTINGS_URL = "https://www.totaljobs.com/jobs/data-engineer/in-{}?radius=0&postedWithin=3"
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


def setup(city):
    """Create required folders for pipeline to run."""
    makedirs(FOLDER_PATHS.format(city, 'page', ''), exist_ok=True)
    makedirs(FOLDER_PATHS.format(
        city, 'page', '/listing'), exist_ok=True)


def run_pipeline(conn):
    """Runs ETL pipeline."""
    for city in CITIES:
        setup(city)
        # run_extract(city)
        path = FOLDER_PATHS.format(city, 'listing', '')
        files = listdir(path)
        for file in files:
            print(file)
            listing_data = get_listing_data(path, file)
            run_load(conn, file.strip('.html'), listing_data)


if __name__ == "__main__":
    try:
        db_conn = db_connection()
        driver = create_driver()
        run_pipeline(db_conn)
    finally:
        db_conn.close()
        driver.quit()
