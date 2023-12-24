"""Unit tests for transform.py"""
import pytest

from ..tests.conftest import FakeListingLocationTuple, FakeSalaryHTML
from pipeline.etl.transform import parse_listing_data, create_key_pairs, extract_job_location, extract_salary_html, extract_digit_from_salary, group_titles_by_category


def test_parse_listing_data_returns_dict(FakeJobListingHTML):
    fake_listing = FakeJobListingHTML
    result = parse_listing_data(fake_listing)
    assert isinstance(result, dict)


@pytest.mark.parametrize("listing_dict_keys", [("url"), ("title"), ("datePosted"),
                                               ("jobLocation")])
def test_parse_listing_data_returns_correct_data(FakeJobListingHTML, listing_dict_keys):
    fake_listing = FakeJobListingHTML
    result = parse_listing_data(fake_listing)
    print(result)
    assert listing_dict_keys in result.keys()


def test_parse_listing_data_returns_None_if_invalid_html(InvalidFakeListingHTML):
    fake_listing = InvalidFakeListingHTML
    result = parse_listing_data(fake_listing)
    assert not result


@pytest.mark.parametrize(("key", "value"), [("url", "https://www.fake_listing-3355"), ("title", "Data Engineer"),
                                            ("datePosted", "2023-10-02T14:34+01:00"), ("NotHere", None)])
def test_create_key_pairs_returns_valid_value_dict_pair(FakeParsedListingDict, key, value):
    fake_parsed_listing = FakeParsedListingDict
    assert create_key_pairs(fake_parsed_listing, key) == value


@pytest.mark.parametrize(("dict", "location"), FakeListingLocationTuple())
def test_extract_job_location_returns_city(dict, location):
    assert extract_job_location(dict) == location


@pytest.mark.parametrize(("html", "salary_text"), FakeSalaryHTML())
def test_extract_salary_html_returns_valid_text(html, salary_text):
    assert extract_salary_html(
        html).strip() == salary_text.lower()


@pytest.mark.parametrize(("sub_string", "expected_output"), [("30k", "30000.0"), ("30", "30.0"), ("20.5", "20.5"),
                                                             ("20.5k", "20500.0"), ("50.2k", "50200.0"), ("£350", "350.0"), ("£25k", "25000.0")])
def test_extract_digit_from_salary(sub_string, expected_output):
    result = extract_digit_from_salary(sub_string)
    assert result == expected_output


# def test_get_title_from_url():
#     "https://www.totaljobs.com/job/lead/lloyd-s-job101669446"
    #  https://www.totaljobs.com/job/servicenow-administrator/la-fosse-associates-ltd-job101501566
    #  https://www.totaljobs.com/job/aws-architect/in-technology-group-limited-job101626759
    #  https://www.totaljobs.com/job/data-business-analyst/hays-job101633330
    #  https://www.totaljobs.com/job/mobile-engineer/cbre-job101316460
#  https://www.totaljobs.com/job/software-developer/oliver-bernard-ltd-job101666872
    #  https://www.totaljobs.com/job/data-cabling-engineer/construkt-rs-limited-job101365211
    #  https://www.totaljobs.com/job/aws-engineer/bright-purple-job101609123
    #  https://www.totaljobs.com/job/cloud-infrastructure-engineer/circle-group-job101676654
#     pass


@pytest.mark.parametrize(("url_title", "title_category"),
                         [("architect java", "Architect"), ("machine learning", "Data Scientist"), ("machine learning Analyst", "Analyst"),
                          ("data analyst", "Analyst"), ("senior software engineer",
                                                        "Software Engineer"), ("ai software developer", "Software Engineer"),
                          ("cloud engineer",
                           "Cloud Engineer"), ("maintenance engineer", "Other"), ("ai engineer", "Data Scientist"), ("safety trainer", "Other"),
                          ("senior devops engineer", "DevOps Engineer"), ("lead",
                                                                          "Other"), ("servicenow administrator", "Other"),
                          ("dev ops engineer", "DevOps Engineer"), ("aws architect",
                                                                    "Architect"), ("data business analyst", "Analyst"),
                          ("mobile engineer", "Other"), ("software developer",
                                                         "Software Engineer"), ("cable engineer", "Other"),
                          ("it security architect", "Architect"), ("data cabling engineer",
                                                                   "Data Engineer"), ("powerbi developer", "Business Intelligence"),
                          ("cloud infrastructure engineer",
                           "Cloud Engineer"), ("lead cloud data engineer", "Data Engineer"),
                          ("software development trainer", "Software Engineer"), ("devops",
                                                                                  "DevOps Engineer"), ("senior test engineer", "Other"),
                          ("embedded software engineer", "Software Engineer"), ("workforce analyst",
                                                                                "Analyst"), ("analyst business intelligence", "Business Intelligence"),
                          ("java developer", "Software Engineer"), (
                              "java software developer", "Software Engineer"), ("ci/cd", "DevOps Engineer"),
                          ("embedded software engineer", "Software Engineer"), (
                              "lead software developer", "Software Engineer"), ("site reliability engineer", "DevOps Engineer"),
                          ("front end developer", "Software Engineer"), ("senior software developer", "Software Engineer"), ("junior data engineer", "Data Engineer")])
def test_group_titles_by_category(url_title, title_category):
    assert group_titles_by_category(
        url_title) == title_category
