"""Unit tests for transform.py"""
import pytest

from ..tests.conftest import FakeListingLocationTuple, FakeSalaryHTMLTests, CreateSalaryHTML
from pipeline.etl.transform import *


def test_parse_listing_data_returns_dict(FakeJobListingHTML):
    result = parse_listing_data(file="fake_file", html=FakeJobListingHTML)
    assert isinstance(result, dict)


@pytest.mark.parametrize("listing_dict_keys", [("url"), ("title"), ("datePosted"),
                                               ("jobLocation")])
def test_parse_listing_data_returns_correct_data(FakeJobListingHTML, listing_dict_keys):
    result = parse_listing_data(file="fake_file", html=FakeJobListingHTML)
    print(result)
    assert listing_dict_keys in result.keys()


def test_parse_listing_data_returns_None_if_invalid_html(InvalidFakeListingHTML):
    result = parse_listing_data(file="fake_file", html=InvalidFakeListingHTML)
    assert not result


@pytest.mark.parametrize(("key", "value"), [("url", "https://www.fake_listing-3355"), ("title", "Data Engineer"),
                                            ("datePosted", "2023-10-02T14:34+01:00"), ("NotHere", None)])
def test_create_key_pairs_returns_valid_value_dict_pair(FakeParsedListingDict, key, value):
    assert create_key_pairs(FakeParsedListingDict, key) == value


@pytest.mark.parametrize(("dict", "location"), FakeListingLocationTuple())
def test_extract_job_location_returns_city(dict, location):
    assert extract_job_location(dict) == location


@pytest.mark.parametrize(("url", "expected_title"), [("https://www.totaljobs.com/job/lead/lloyd-s-job101669446", "lead"),
                                                     ("https://www.totaljobs.com/job/aws-architect/in-technology-group-limited-job101626759", "aws architect"),
                                                     ("https://www.totaljobs.com/job/data-business-analyst/hays-job101633330",
                                                      "data business analyst"),
                                                     ("https://www.totaljobs.com/job/mobile-engineer/cbre-job101316460", "mobile engineer"),
                                                     ("https://www.totaljobs.com/job/software-developer/oliver-bernard-ltd-job101666872", "software developer"),
                                                     ("https://www.totaljobs.com/job/data-cabling-engineer/construkt-rs-limited-job101365211",
                                                      "data cabling engineer"),
                                                     ("https://www.totaljobs.com/job/aws-data-engineer/bright-purple-job101609123", "aws data engineer"),
                                                     ("job/data/",
                                                      "data"), ("https//www.invalid.com", None), ("www.alsoinvalid.com//do-not-extract/", None),
                                                     ("www.fakesite/job/data-engineer////",
                                                      "data engineer"),
                                                     ("https://www.totaljobs.com/job/cloud-infrastructure-engineer/circle-group-job101676654", "cloud infrastructure engineer")])
def test_get_title_from_url(url, expected_title):
    title = get_title_from_url(url)
    assert title == expected_title


@pytest.mark.parametrize(("url_title", "listing_title", "title_category"),
                         [
    ("engineering-apprentice", "Data Engineering Apprentice", "Data Engineer"),
    ("digital-engineer", "Digital Data Engineer", "Data Engineer"),
    ("architect java", "Solution Architect Java", "Architect"),
    ("machine learning", "Senior Machine Learning Engineer", "Data Scientist"),
    ("machine learning Analyst", "Machine Learning Analyst", "Analyst"),
    ("data analyst", "Junior Data Analyst", "Analyst"),
    ("senior software engineer", "Senior Software Engineer", "Software Engineer"),
    ("ai software developer", "AI Software Developer", "Software Engineer"),
    ("cloud engineer", "Cloud Engineer - Graduate", "Cloud Engineer"),
    ("maintenance engineer",
     "Shift Data Centre Maintenance Engineer - Slough", "Data Engineer"),
    ("ai engineer", "AI Engineer", "Data Scientist"),
    ("safety trainer", "Highway Inspection / Road Safety Trainer", "Other"),
    ("senior devops engineer", "Senior DevOps Engineer", "DevOps Engineer"),
    ("lead", "Fraud Lead", "Other"),
    ("servicenow administrator", "ServiceNow Systems Administrator", "Other"),
    ("dev ops engineer", "DevOps Systems Engineer", "DevOps Engineer"),
    ("aws architect", "AWS Solutions Architect", "Architect"),
    ("data business analyst", "Data Business Analyst - Operations", "Analyst"),
    ("mobile engineer", "Mobile Systems Engineer", "Software Engineer"),
    ("software developer", "Full Stack Software Developer", "Software Engineer"),
    ("cable engineer", "Cable System Design Engineer", "Other"),
    ("it security architect", "IT Security Architect", "Architect"),
    ("data cabling engineer", "Data Cabling and Network Engineer", "Data Engineer"),
    ("powerbi developer", "PowerBI Solutions Developer", "Business Intelligence"),
    ("cloud infrastructure engineer",
     "Cloud Infrastructure and Operations Engineer", "Cloud Engineer"),
    ("lead cloud data engineer", "Lead Cloud Data Engineer", "Data Engineer"),
    ("software development trainer",
     "Software Development and Training Specialist", "Other"),
    ("devops", "DevOps and Infrastructure Engineer", "DevOps Engineer"),
    ("senior test engineer", "Senior Software Test Engineer", "Software Engineer"),
    ("embedded software engineer", "Embedded Software Engineer", "Software Engineer"),
    ("workforce analyst", "Workforce Planning Analyst", "Analyst"),
    ("analyst business intelligence",
     "Business Intelligence Analyst", "Business Intelligence"),
    ("java developer", "Java Software Developer", "Software Engineer"),
    ("java software developer", "Java Full-Stack Developer", "Software Engineer"),
    ("ci/cd", "CI/CD Automation Engineer", "DevOps Engineer"),
    ("embedded software engineer",
     "Embedded Systems Software Engineer", "Software Engineer"),
    ("lead software developer", "Lead Software Developer", "Software Engineer"),
    ("site reliability engineer", "Site Reliability Engineer", "DevOps Engineer"),
    ("front end developer", "Front End Web Developer", "Software Engineer"),
    ("senior software developer", "Senior Full Stack Developer", "Software Engineer"),
    ("junior data engineer", "Junior Data Engineer - Analytics",
     "Data Engineer"),    ("3rd line engineer", "3rd Line Engineer", "Other"),
    ("senior data professional",
     "Senior Data Management Professional - Data Engineering", "Data Engineer"),
    ("bi developer", "BI Developer (Hybrid)", "Business Intelligence"),
    ("data team lead", "Asset Data Team Lead", "Other"),
    ("multi skilled engineer", "Multi-Skilled Engineer (Central Rivers)", "Other"),
    ("business intelligence engineer",
     "Business Intelligence BI Engineer", "Business Intelligence"),
    ("data analyst", "Data Analyst", "Analyst"),
    ("commercial gas engineer", "Mobile Commercial Gas Engineer", "Other"),
    ("senior cloud engineer",
     "Senior Cloud Engineer - AWS - Remote Working", "Cloud Engineer"),
    ("application support officer",
     "Controcc Application Support Officer", "Other"),
    ("data engineer", "Data Engineer", "Data Engineer"),
    ("distribution engineer", "Distribution Data Engineer", "Data Engineer"),
    ("data scientist", "Data Scientist", "Data Scientist"),
    ("senior developer", "Senior Developer", "Software Engineer"),
    ("junior servicenow developer",
     "Junior Service Now Developer", "Software Engineer"),
    ("erp analyst", "ERP / SQL Support Analyst", "Analyst"),
    ("senior test engineer", "Senior Test Engineer", "Other"),
    ("it business analyst", "IT Business Analyst", "Analyst"),
    ("sales executive", "Sales Executive - North-West England", "Other"),
    ("devops engineer", "DevOps Engineer", "DevOps Engineer"),
    ("data base administrator",
     "Database Administrator - £60,000 DOE - Leeds Area (Hybrid)", "Database Administrator"),
    ("senior business intelligence developer",
     "Senior Business Intelligence Developer", "Business Intelligence"),
    ("data apprenticeship", "Junior Data Analyst Apprenticeship", "Analyst"),
    ("analytics manager", "Analytics Manager",
     "Analyst"), ("devops", "UKIC Infra DevOps", "DevOps Engineer"),
    ("software design engineer",
     "Electrical and Software Design Engineer", "Software Engineer"),
    ("junior full stack software developer",
     "Junior Full Stack Software Developer", "Software Engineer"),
    ("performance analyst", "Lead Performance Analyst", "Analyst"),
    ("digital engineer", "Digital Data Engineer", "Data Engineer"),
    ("net developer", ".Net Developer", "Software Engineer"),
    ("senior react engineer", "Senior React Frontend Engineer", "Software Engineer"),
    ("software developer", "Software Developer", "Software Engineer"),
    ("workforce analyst", "Workforce Analyst", "Analyst"),
    ("data scientist", "Data Scientist", "Data Scientist"),
    ("business intelligence analyst",
     "Business Intelligence Analyst", "Business Intelligence"),
    ("senior science manager", "Senior Data Science Manager (GenAI)", "Data Scientist"),
    ("data scientist ml researcher",
     "Data Scientist / ML Researcher", "Data Scientist"),
    ("senior insight analyst", "Senior Insight Analyst", "Analyst"),
    ("scheduler", "Domestic Connections Scheduler", "Other"),
    ("data apprenticeship", "Data Analyst Apprenticeship", "Analyst"),
    ("marketing analyst", "Marketing Analyst", "Analyst"),
    ("master data manager", "Pricing Analyst & Master Data Manager", "Analyst"),
    ("operational analyst", "Operational Analyst Principal", "Analyst"),
    ("risk reporting analyst",
     "Liquidity Risk - Analytics and Reporting - Analyst - Birmingham", "Analyst"),
    ("reporting analyst", "BI Reporting Analyst", "Analyst"),
    ("customer insights analyst", "Customer Insights Analyst", "Analyst"),
    ("senior data analyst", "Senior Data Analyst", "Analyst"),
    ("information manager", "Information Analyst Manager", "Analyst"),
    ("bi analyst", "BI Analyst", "Analyst"),
    ("deputy head", "Deputy Head of Operational Performance", "Other"),
    ("mid devops engineer", "Mid-Snr DevOps Engineer", "DevOps Engineer"),
    ("systems engineer", "Systems Engineer", "Software Engineer"),
    ("solution architect", "Solution Architect", "Architect"),
    ("site reliability engineer",
     "Operations Site Reliability Engineer", "DevOps Engineer"),
    ("internal audit associate",
     "Internal Audit -Regional Audit Associate - Birmingham", "Other"),
    ("network architect", "Network Management System Architect", "Architect"),
    ("cyber security architect",
     "CyberSecurity Architect - Azure - Home Working", "Architect"),
    ("engineer javascript", "Cloud Engineer - Javascript/Typescript", "Cloud Engineer"),
    ("cloud native engineer", "Mid-Level Cloud Native Engineer", "Cloud Engineer"),
    ("senior support engineer", "Senior Support Desk Engineer", "Other"),
    ("solutions architect", "Solutions Architect", "Architect"),
    ("senior data architect", "Senior Data Domain Architect", "Architect"),
    ("devops engineer", "Graduate DevOps Engineer", "DevOps Engineer"),
    ("cloud engineer", "Systems & Cloud Engineer (DevOps)", "Cloud Engineer"),
    ("cloud engineer", "Cloud Engineer", "Cloud Engineer"),
    ("devops engineer contract",
     "DevOps Engineer - Contract Inside IR35", "DevOps Engineer"),
    ("devops engineer", "DevOps Engineer", "DevOps Engineer"),
    ("senior devops engineer", "Senior DevOps Engineer", "DevOps Engineer"),
    ("manufacturing administrator", "Manufacturing Administrator", "Other"),
    ("azure devops engineer", "Azure DevOps Engineer - Essex - £500pd", "DevOps Engineer"),
    ("data base administrator", "Database Administrator", "Database Administrator"),
    ("communication engineer", "Communication Engineer", "Other"),
    ("business systems analyst", "Business Systems Service Desk Analyst", "Analyst"),
    ("sharepoint administrator", "Sharepoint Administrator", "Other"),
    ("application developer", "Application Developer", "Software Engineer"),
    ("senior data architect", "Senior Data Domain Architect", "Architect"),
    ("cloud solutions engineer", "Cloud Solutions Design Engineer", "Cloud Engineer"),
    ("solution architect", "Solution Architect", "Architect"),
    ("senior infrastructure engineer",
     "Senior Cloud Infrastructure Engineer", "Cloud Engineer"),
    ("cloud engineer", "Systems & Cloud Engineer (DevOps)", "Cloud Engineer"),
    ("infrastructure engineer",
     "Infrastructure Engineer- Security Platforms", "Other"),
    ("cloud engineer", "Cloud Engineer", "Cloud Engineer"),
    ("presales engineer", "Presales Consultant System Engineer IV", "Other"),
    ("devops engineer contract",
     "DevOps Engineer - Contract Inside IR35", "DevOps Engineer"),
    ("devops engineer", "DevOps Engineer", "DevOps Engineer"),
    ("senior devops engineer", "Senior DevOps Engineer", "DevOps Engineer")
])
def test_group_titles_by_category(url_title, listing_title, title_category):
    assert group_titles_by_category(
        url_title, listing_title) == title_category


@pytest.mark.parametrize(("html", "salary_text"), FakeSalaryHTMLTests())
def test_extract_salary_html_returns_valid_text(html, salary_text):
    assert extract_salary_html(
        html).strip() == salary_text.lower()


@pytest.mark.parametrize(("salary_text", "expected_output"), [("Up to £24000 per annum + £29k OTE + Benefits", ["24000.0"]), ("From £40,000 to £55,000 per annum", ["40000.0", "55000.0"]),
                                                              ("£60000.00 - £75000.00 per annum",
                                                               ["60000.0", "75000.0"]), ("£70000 - £80000 per annum", ["70000.0", "80000.0"]), ("30k", ["30000.0"]), ("30", ["30.0"]), ("20.5", ["20.5"]), ("$27k", ["27000.0"]), ("£103.2k", ["103200.0"]),
                                                              ("20.5k", ["20500.0"]), ("50.2k", ["50200.0"]), ("£350", [
                                                                  "350.0"]), ("£25k", ["25000.0"]), ("Competitive", None),
                                                              ("£70000.0 - £105000.0 per annum + £70-105,000 plus package", [
                                                                  "70000.0", "105000.0"]),
                                                              ("£400 - £500 per day", ["400.0", "500.0"]),             ("The salary range in Colorado for this role is from USD $123,500 - $185,500",
                                                                                                                        ["123500.0", "185500.0"]),
                                                              ("Pay Range: 12.00 - 16.00 plus 30k bonus", [
                                                               "12.0", "16.0"]),
                                                              ("20-25k plus 30k bonus",
                                                               ["20000.0", "25000.0"]),
                                                              ("£22.5k - 30k and 30k bonus",
                                                               ["22500.0", "30000.0"]),
                                                              ("50k to 69 per annum is the salary", [
                                                               "50000.0", "69000.0"]),
                                                              ("44k", [
                                                               "44000.0"]),
                                                              ("52.4k-74.2k",
                                                               ["52400.0", "74200.0"]),
                                                              ("22.4k-22.7", ["22400.0", "22700.0"]
                                                               ),
                                                              ("£20-30k plus more", ["20000.0", "30000.0"])])
def test_extract_floats_from_salary(salary_text, expected_output):
    result = extract_floats_from_salary(salary_text)
    assert result == expected_output


@pytest.mark.parametrize("lower,upper,salary_text, expected_type", [
    (30000.0, 30000.0, "£30,000 per annum",
     "year"), (70000.0, 75000.0, "70 - 75K + 6% Pension, Private health 25 days etc", "year"),
    (50000.0, 50000.0, "£50,000 annually", "year"),
    (30000.0, 30000.0, "€30,000 a year", "year"),
    (30.0, 30.0, "$30 per hour", "hour"),
    (500.0, 500.0, "€500 monthly", "month"),
    (30000.0, 40000.0, "30-40k per year", "year"),
    (24000.0, 24000.0, "Up to £24000 per annum + £29k OTE + Benefits", "year"),
    (30000.0, 30000.0, "$30k", "year"),
    (30.0, 30.0, "$30", "unspecified")
])
def test_extract_salary_type(lower, upper, salary_text, expected_type):
    assert extract_salary_type(lower, upper, salary_text) == expected_type


@pytest.mark.parametrize("salary_html, expected_salary", [
    (CreateSalaryHTML("£30,000 per annum"), {
     'lower': "30000.0", 'upper': "30000.0", 'salary_type': 'year'}),
    (CreateSalaryHTML("€40,000 to €50,000 annually"), {
     'lower': "40000.0", 'upper': "50000.0", 'salary_type': 'year'}),
    (CreateSalaryHTML("$20 - $25 per hour"),
     {'lower': "20.0", 'upper': "25.0", 'salary_type': 'hour'}),
    (CreateSalaryHTML("Competitive salary"), {
     'lower': None, 'upper': None, 'salary_type': 'competitive'}),
    (CreateSalaryHTML("£35k - £40k per year"),
     {'lower': "35000.0", 'upper': "40000.0", 'salary_type': 'year'})
])
def test_extract_job_salary(salary_html, expected_salary):
    assert extract_job_salary(salary_html) == expected_salary
