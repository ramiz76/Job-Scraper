"""Unit tests for transform.py"""
import pytest

from tests.conftest import FakeJobListingHTML, InvalidFakeListingHTML, FakeParsedListingDict
from etl.transform import parse_listing_data, create_key_pairs, extract_job_details


def test_parse_listing_data_returns_dict():
    fake_listing = FakeJobListingHTML()
    result = parse_listing_data(fake_listing)
    assert isinstance(result, dict)


@pytest.mark.parametrize("listing_dict_keys", [("url"), ("title"), ("datePosted"),
                                               ("jobLocation")])
def test_parse_listing_data_returns_correct_data(listing_dict_keys):
    fake_listing = FakeJobListingHTML()
    result = parse_listing_data(fake_listing)
    print(result)
    assert listing_dict_keys in result.keys()


def test_parse_listing_data_returns_None_if_invalid_html():
    fake_listing = InvalidFakeListingHTML()
    result = parse_listing_data(fake_listing)
    assert not result


@pytest.mark.parametrize(("key", "value"), [("url", "https://www.fake_listing-3355"), ("title", "Data Engineer"),
                                            ("datePosted", "2023-10-02T14:34+01:00"), ("NotHere", None)])
def test_create_key_pairs_returns_valid_value_dict_pair(key, value):
    fake_parsed_listing = FakeParsedListingDict()
    assert create_key_pairs(fake_parsed_listing, key) == value
