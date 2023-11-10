"""Run the the full ETL pipeline."""
from datetime import datetime
from os import environ, listdir, makedirs

from extract import create_driver, run_extract
from transform import get_listing_data
from load import run_load

DATE = datetime.now().strftime("%y_%m_%d")
FULL_LISTING_URL = "https://www.totaljobs.com/{}"
ALL_LISTINGS_URL = "https://www.totaljobs.com/jobs/data-engineer/in-{}?radius=0&postedWithin=3"
CITIES = ['london', 'bristol', 'manchester']
FOLDER_PATHS = "{}/{}"


def setup(city):
    """Create required folders for pipeline to run."""
    makedirs(FOLDER_PATHS.format(city, 'page', ''), exist_ok=True)
    makedirs(FOLDER_PATHS.format(
        city, 'page', '/listing'), exist_ok=True)


def run_pipeline():
    """Runs ETL pipeline."""
    for city in CITIES:
        setup(city)
        run_extract(driver, city)
        path = FOLDER_PATHS.format(city, 'listing', '')
        files = listdir(path)
        for file in files:
            listing_data = get_listing_data(path, file)
            run_load(file.strip('.html'), listing_data)


if __name__ == "__main__":
    try:
        driver = create_driver()
        run_pipeline()
    finally:
        driver.close()