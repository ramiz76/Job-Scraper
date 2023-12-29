"""Run the the full ETL pipeline."""
from os import environ, listdir, rename
from shutil import move
from datetime import datetime

from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection

from extract import create_driver, run_extract, setup
from transform import get_listing_data
from load import run_load

DATE = datetime.now().strftime("%y_%m_%d")
CITIES = ['bristol', 'manchester', 'birmingham', 'london']
FOLDER_PATHS = "{}/{}"
JOB_TITLES = ["data-engineer", "software-engineer",
              "data-analyst", "data-scientist", "cloud-engineer", "devops-engineer",
              "database-administrator"]


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
        for job_title in JOB_TITLES:
            print(f"Processing job title: {job_title}")
            run_extract(city, job_title)
            path = FOLDER_PATHS.format(city, 'listing', '')
            webpage_path = FOLDER_PATHS.format(city, 'page', '')
            files = listdir(path)
            print(f"loading {job_title} job listings")
            for file in files:
                try:
                    listing_data = get_listing_data(path, file)
                    run_load(conn, file.strip('.html'), listing_data)
                except (AttributeError, TypeError) as err:
                    print(f"Error processing {file}: {err}")
                    continue
                move(f"{path}/{file}", f"archive/{path}/{file}")
            for page in listdir(webpage_path):
                new_page = page
                new_page = f"{job_title}-{page}"
                rename(f"{webpage_path}/{page}", f"{webpage_path}/{new_page}")
                move(f"{webpage_path}/{new_page}",
                     f"archive/{webpage_path}/{new_page}")


if __name__ == "__main__":
    try:
        db_conn = db_connection()
        driver = create_driver()
        run_pipeline(db_conn)
    finally:
        db_conn.close()
        driver.quit()
