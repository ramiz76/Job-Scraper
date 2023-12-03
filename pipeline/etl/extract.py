"""
This module web scrapes job listing data from a specified job listing website to be stored in HTML format.
"""
from os import makedirs
from time import sleep
from datetime import datetime
from random import randint
import re

from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DATE = datetime.now().strftime("%y_%m_%d")
FULL_LISTING_URL = "https://www.totaljobs.com/{}"
ALL_LISTINGS_URL = "https://www.totaljobs.com/jobs/data-engineer/in-{}?radius=0&postedWithin=3"
FOLDER_PATHS = "{}/{}"


def create_driver() -> webdriver:
    """
    Create and return a headless Chrome webdriver.
    """
    option = Options()
    option.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=option)
    return driver


def accept_cookies(driver) -> None:
    """
    Accept cookies from pop ups in the webdriver.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ccmgt_explicit_accept"))
        ).click()
        sleep(randint(2, 6))
    except TimeoutException:
        return None
    return None


def setup(city):
    """Create required folders for pipeline to run."""
    listing_path = FOLDER_PATHS.format(
        city, 'listing')
    webpage_path = FOLDER_PATHS.format(city, 'page', '')
    makedirs(webpage_path, exist_ok=True)
    makedirs(listing_path, exist_ok=True)
    makedirs(f"archive/{webpage_path}", exist_ok=True)
    makedirs(f"archive/{listing_path}", exist_ok=True)


def make_listings_request(driver: webdriver, url: str, attribute: str = "") -> str:
    """
    Perform a GET request to retrieve HTML data of a job listing website.
    Returns the page source if successful, otherwise returns None.
    """
    payload = url.format(attribute)
    driver.get(payload)
    accept_cookies(driver)
    if driver.title:
        return driver.page_source
    return None


def get_webpages_href(html: BeautifulSoup) -> list:
    """
    Extract href for each page of the job listing website.
    Returns a list of href strings.
    """
    pages_href = [page.get('href')
                  for page in html.find_all('a', class_='res-1joyc6q')]
    return pages_href


def get_listings_href(html: BeautifulSoup) -> list:
    """
    Extract href for the full job description webpage of each job listing.
    Returns a list of href strings.
    """
    jobs = html.find_all(class_="res-1tps163")
    listings_href = [
        job.find('a', class_='res-1na8b7y').get('href') for job in jobs]
    return listings_href


def create_html(city: str, attribute: str, identity: str, response: str) -> None:
    """
    Create an HTML file to store GET request data from the website.
    """
    with open(f'{city}/{attribute}/{identity}.html', "w") as html_file:
        html_file.write(response)


def handle_listing_extraction(driver: webdriver, job_id: tuple, city: str) -> None:
    """
    Extract HTML data from the full job listing webpage.
    """
    accept_cookies(driver)
    listing = driver.page_source
    if job_id:
        create_html(city, 'listing', job_id.group(), listing)


def process_webpage(driver: webdriver, city: str, attribute: str, identity: str, html: str) -> None:
    """
    Navigate through each job listing of the webpage to extract HTML data using automated clicking.
    """
    create_html(city, attribute, identity, html)
    listings_href = get_listings_href(BeautifulSoup(html, 'html.parser'))
    for href in listings_href:
        try:
            job_id = get_job_id(href)
            listing_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"a[href='{href}']"))
            )
            listing_element.click()
            sleep(randint(2, 6))
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                handle_listing_extraction(driver, job_id, city)
                driver.close()
                sleep(2)
                driver.switch_to.window(driver.window_handles[0])
            else:
                handle_listing_extraction(driver, job_id, city)
                sleep(2)
                driver.back()
        except TimeoutException as err:
            print("Could not load listing data.", err)
            continue


def get_job_id(href: str) -> str:
    """
    Use regex to retrieve the job_id from a job listing href.
    Returns a regex Match object if found, None otherwise.
    """
    return re.search(r'job(\d+)', href)


def run_extract(city) -> None:
    """check if for load"""
    try:
        driver = create_driver()
        webpage = make_listings_request(driver, ALL_LISTINGS_URL, city)
        if webpage:
            process_webpage(driver, city, 'page', f'1-{DATE}', webpage)
            webpages = get_webpages_href(
                BeautifulSoup(webpage, 'html.parser'))
            for i, url in enumerate(webpages):
                page_num = str(i+2)
                webpage = make_listings_request(driver, url, "")
                if webpage:
                    process_webpage(driver, city, 'page',
                                    f'{page_num}-{DATE}', webpage)
    except:
        print(f"Error processing {city}")
    finally:
        driver.quit()
