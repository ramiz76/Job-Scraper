"""Unit tests for extract.py"""

from conftest import FakeListingURL, FakeDriver, FakeWebpageHref, FakeWebpageNoHref
from extract import make_listings_request, get_webpages_href, get_job_id


def test_successful_webpage_request_returns_string():
    url = FakeListingURL()
    fake_driver = FakeDriver()
    fake_driver.title = "Data Engineer Jobs"
    response = make_listings_request(fake_driver, url, "")
    assert isinstance(response, str)


def test_unsuccessful_webpage_request_returns_None():
    url = FakeListingURL()
    fake_driver = FakeDriver()
    fake_driver.title = ""
    response = make_listings_request(fake_driver, url, "")
    assert not response


def test_get_webpages_href_returns_valid_url():
    fake_webpage = FakeWebpageHref()
    response = get_webpages_href(fake_webpage)
    assert (href.startswith("https://www.") for href in response)


def test_get_webpages_returns_None_if_no_additional_website_pages():
    fake_webpage = FakeWebpageNoHref()
    response = get_webpages_href(fake_webpage)
    assert not response


# Use parameters for this test
def test_job_id_retrieved_from_listing_href():
    fake_href = "https://www.fake_listing-job101156323"
    job_id = get_job_id(fake_href)
    assert job_id.group() == "job101156323"


# Use parameters for this test
def test_no_job_id_in_listing_href_returns_None():
    fake_href = "https://www.fake_listing-101156323"
    job_id = get_job_id(fake_href)
    assert job_id == None


def test_get_listings_href():
    ""
