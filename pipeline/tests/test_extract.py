"""Unit tests for extract.py"""
import pytest

from tests.conftest import FakeListingURL, FakeDriver, FakeWebpageHref, FakeWebpageNoHref, FakeWebpageListings
from etl.extract import make_listings_request, get_webpages_href, get_job_id, get_listings_href


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


@pytest.mark.parametrize("valid_job_id", [("job101156323"), ("job01153433"), ("job323"), ("job1")])
def test_job_id_retrieved_from_listing_href(valid_job_id):
    fake_href = f"https://www.fake_listing-{valid_job_id}"
    job_id = get_job_id(fake_href)
    assert job_id.group() == valid_job_id


@pytest.mark.parametrize("invalid_job_id", [("j10113"), ("job-03"), ("323"), ("job")])
def test_no_job_id_in_listing_href_returns_None(invalid_job_id):
    fake_href = f"https://www.fake_listing-{invalid_job_id}"
    job_id = get_job_id(fake_href)
    assert job_id == None


@pytest.mark.parametrize("expected_href", [("fake_href"), ("/job/data-engineer/develop-job101378062"), ("sfjksfje23!!@342|")])
def test_get_listings_href(expected_href):
    fake_html = FakeWebpageListings(expected_href)
    listings_href = get_listings_href(fake_html)
    print(listings_href)
    assert isinstance(listings_href, list)
    assert all(href == expected_href for href in listings_href)
