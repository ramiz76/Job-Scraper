"""Unit tests for extract.py"""

from unittest.mock import MagicMock, patch

from conftest import FakeListingURL, FakeDriver
from extract import make_listings_request, get_webpages_href


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
    pass
