import os
import pathlib
from time import sleep
from datetime import datetime
from random import randint
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

DATE = datetime.now().strftime("%y_%m_%d")
FULL_LISTING_URL = "https://www.totaljobs.com/{}"
ALL_LISTINGS_URL = "https://www.totaljobs.com/jobs/data-engineer/in-{}?radius=0&postedWithin=3"
CITIES = ['london', 'bristol', 'manchester']


# def get_html_path() -> str:
#     """Used for Developer to test using local html containing listing search page."""
#     path = os.path.abspath('../empty.html')
#     url = pathlib.Path(path).as_uri()
#     return url


def create_driver() -> webdriver:
    """Creates web driver to retrieve job listings data from the webpage."""
    option = Options()
    # option.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=option)
    return driver


def make_listings_request(driver: webdriver, url: str, attribute: str = "") -> str | None:
    """Perform GET request to retrieve job listings data from webpage in HTML format."""
    payload = url.format(attribute)
    driver.get(payload)
    sleep(randint(2, 6))
    if driver.title != "":
        return driver.page_source
    return


def get_webpages_href(html: BeautifulSoup) -> list|None:
    """Extract href for each webpage of the job listings web application"""
    pages_href = [page.get('href')
                  for page in html.find_all('a', class_='res-1joyc6q')]
    return pages_href


def get_listings_href(html: BeautifulSoup) -> list|None:
    """Extract href for each listings full job description webpage"""
    jobs = html.find_all(class_="res-1tps163")
    listings_href = [job.find('a',class_='res-1na8b7y').get('href') for job in jobs]
    return listings_href


def create_html(city: str, attribute: str, identity: str, response: str):
    """Create HTML file to store GET request data from web application."""
    with open(f'{city}/{attribute}/{identity}.html', "w") as html_file:
        html_file.write(response)


def process_webpage(driver: webdriver, city: str, attribute: str, identity: str, html: str) -> None:
    create_html(city, attribute, identity, html)
    listings_href = get_listings_href(BeautifulSoup(html, 'html.parser'))
    for href in listings_href:
        listing = make_listings_request(driver, FULL_LISTING_URL, href)
        job_id = get_job_id(href)
        if job_id:
            create_html(city, 'listing', job_id.group(), listing)


def get_job_id(href: str) -> str | None:
    """Uses Regex to retrieve job_id from job listing href."""
    return (re.search(r'job(\d+)', href))


def execute():
    try:
        driver = create_driver()
        "created driver"
        for city in CITIES:
            print(city, 'processing')
            webpage = make_listings_request(driver, ALL_LISTINGS_URL, city)
            process_webpage(driver, city, 'page', f'1-{DATE}', webpage)
            webpages = get_webpages_href(BeautifulSoup(webpage, 'html.parser'))
            for i, url in enumerate(webpages):
                page_num = str(i+2)
                webpage = make_listings_request(driver, url, "")

                process_webpage(driver, city, 'page',
                                f'{page_num}-{DATE}', webpage)
    finally:
        driver.quit()


if __name__ == "__main__":
    # execute()
    pass
