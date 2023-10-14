"Extract"

from os import environ

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

ZENROWS_URL = 'https://api.zenrows.com/v1/'
INDEED_PAGES_URL = 'https://uk.indeed.com/jobs?q=junior+data+engineer&l=London%2C+Greater+London&start='
FULL_LISTING_URL = 'https://uk.indeed.com/viewjob'


def make_listings_request(url, identity):
    """Perform GET request to retrieve job listing summaries for first three indeed pages."""
    params = {
        'url': f'{url}{identity}',
        'apikey': environ.get("SCRAPE_API_KEY")
    }
    response = (requests.get(
        ZENROWS_URL, params=params)).text
    parsed_response = BeautifulSoup(response, 'html.parser')
    return parsed_response


def create_html(data, response, identity) -> None:  # DEVELOPER USE
    """Create HTML file for job listings summary GET response."""
    response = response.prettify()
    with open(f'{data}/{identity}.html', "w") as html_file:
        html_file.write(response)


def extract_full_listing_url(response):
    """Iterate through each job listing and processes it."""
    all_listings_url = []
    all_listings = response.find_all(
        'div', class_='css-1m4cuuf e37uo190')

    for listing in all_listings:
        url = listing.find('a')['href'].strip('/rc/clk')
        all_listings_url.append(url)
    return all_listings_url


def process_listings_pages() -> None:
    """Process first three job listings pages"""
    for i in range(0, 11, 10):
        print(f'Retrieving listings from page {int(i/10)+1}')
        response = make_listings_request(INDEED_PAGES_URL, i)
        create_html('page', response, i)
        all_listings_url = extract_full_listing_url(response)
        process_full_listings(all_listings_url)


def process_full_listings(all_listings_url):
    """Process full listing data for each job"""
    for url in all_listings_url:
        response = make_listings_request(FULL_LISTING_URL, url)
        create_html('listing', response, url)


if __name__ == "__main__":
    load_dotenv()
    process_listings_pages()
