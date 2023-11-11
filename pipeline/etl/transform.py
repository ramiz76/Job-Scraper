"""
This module parses job listing data from the web scraped job listing HTML.
"""

import json
import re
from os import environ, listdir
from datetime import datetime

from bs4 import BeautifulSoup
import spacy
from dotenv import load_dotenv


DATE = datetime.now().strftime("%y_%m_%d")
PERIOD = {'year': ['year', 'annum', 'annual', 'annually', 'p.a'],
          'month': ['month', 'monthly'],
          'day': ['day', 'daily'],
          'hour': ['hour', 'hourly']}


def open_html_file(file_path: str) -> BeautifulSoup:
    """Open job listing html file and return as BeautifulSoup Object."""
    with open(file_path) as html_file:
        html = BeautifulSoup(html_file, 'html.parser')
    return html


def parse_listing_data(html: BeautifulSoup) -> dict:
    """Extract full job listing data and return in JSON format."""
    try:
        listing_data = (html.find("script", id="jobPostingSchema")).string
        listing_data = json.loads(listing_data)
    except AttributeError:
        listing_data = None
    return listing_data


def create_key_pairs(data: dict, key: str) -> str:
    """Pass in keys to extract its value pair from job listings dict."""
    try:
        return data.get(key)
    except (KeyError, AttributeError):
        return None


def extract_job_location(data):
    """Extract city of job listing from varied dictionary location."""
    try:
        city = (data.get('jobLocation', {}).get('address', {}).get('addressLocality') or
                data.get('jobLocation', {}).get('address', {}).get('addressRegion'))
    except (KeyError, AttributeError):
        city = None
    return city


def extract_job_details(html, data: dict) -> dict:
    """Extract key details of job listing."""
    job_details = {}
    job_details['title'] = create_key_pairs(data, 'title')
    job_details['url'] = create_key_pairs(data, 'url')
    job_details['date'] = create_key_pairs(data, 'datePosted')
    job_details['industry'] = create_key_pairs(data, 'industry')
    job_details['employment_type'] = create_key_pairs(data, 'employmentType')

    job_details['city'] = extract_job_location(data)
    job_details['salary'] = extract_job_salary(html)
    return job_details


# def extract_job_salary(html: BeautifulSoup):
#     """Extract job salary from salary html tag."""
#     try:
#         salary = (html.find('li', class_='salary')).find(
#             'div').get_text()
#     except (KeyError, ArithmeticError):
#         return None
#     if salary:
#         if 'competitive' in salary.lower():
#             return 'competitive'
#         money_labels = find_money_labels(salary)
#         ranges = find_numbers_from_salary_text(money_labels)
#         period = extract_salary_type(salary)
#     if ranges:
#         return find_salary_range(ranges, period)
#     return None


def extract_digit_from_salary(element):
    """Return string if all characters are digits, excluding currency."""
    try:
        num = re.sub(f'[£$€,]', '', element)
        num = re.sub(f'k', '000', num)
        decimal = num.find('.')
        if decimal != -1:
            num = num[:decimal]
        if num.isdigit():
            return num
    except ValueError:
        return


def find_numbers_from_salary_text(money_entities):
    """Locate numbers from all tokens with the texts tagged with MONEY label."""
    ranges = []
    for money in money_entities:
        if len(money.replace(" ", "")) < len(money):
            for element in money.split():
                num = extract_digit_from_salary(element)
                if num:
                    ranges.append(num)
        else:
            num = extract_digit_from_salary(money)
            if num:
                ranges.append(num)
    return ranges


def extract_salary_html(html: BeautifulSoup) -> str:
    """Extract job salary text from salary html tag."""
    try:
        salary_html = html.find('section', class_='job-summary')
        salary_text = salary_html.find(
            'li', class_='salary icon').get_text()
        return salary_text.lower()
    except AttributeError:
        return None


def extract_job_salary(html: BeautifulSoup) -> list:
    salary_text = extract_salary_html(html)
    if not salary_text:
        return None
    if 'competitive' in salary_text:
        return ['competitive', 'competitive', None]

    money_entities = [ent.text for ent in NLP_LG(
        salary_text).ents if ent.label_ == 'MONEY']
    ranges = find_numbers_from_salary_text(money_entities)
    period = extract_salary_type(salary_text)
    return find_salary_range(ranges, period)


def find_salary_range(ranges: list, period: str) -> list:
    """Return salary range based on extracted numbers."""
    if not ranges:
        return None
    if len(ranges) == 1:
        return [ranges[0], ranges[0], period]
    return [min(ranges), max(ranges), period]


def extract_salary_type(salary: str) -> str:
    """Locate salary type from salary text of job listing."""
    for key, value in PERIOD.items():
        if any(period_word in salary for period_word in value):
            return key
    return None


def extract_company_details(data: dict) -> dict:
    """Extract hiring company key details."""
    try:
        hiring_org = data.get('hiringOrganization')
        hiring_company = {'name': hiring_org.get('name'),
                          'type': hiring_org.get('@type'),
                          'url': hiring_org.get('url')}
    except KeyError:
        return None
    return hiring_company


def parse_job_description(data: dict) -> list:
    """Extract job description from html tags and store in a list."""
    desc = data.get('description')
    desc = BeautifulSoup(desc, 'html.parser')
    p_elements = desc.find_all('p')
    p_texts = [p.text for p in p_elements]
    li_elements = desc.find_all('li')
    listed_desc = [li.text for li in li_elements]
    job_description = p_texts
    job_description.extend(listed_desc)
    return job_description


def open_skills_json() -> set:
    """Retrieve all skill names stored in JSON file."""
    with open('pipeline/skills_filtered.json', 'r') as skills_json:
        data = json.load(skills_json)
    skills_set = {key.lower() for key in data.keys()}
    return skills_set


def extract_skills_from_description(job_desc: list) -> dict:
    skills_dict = {}
    for sentence in job_desc:
        skills_list = []
        sentence = NLP_SKILLS(sentence)
        for ent in sentence.ents:
            skills_list.append([ent.text, ent.label_])
        skills_dict[sentence.text] = skills_list
    return skills_dict


def load_json(skills):
    with open(f'model-output/{DATE}-model_output.json', 'w') as json_file:
        json.dump(skills, json_file, indent=4)


def testing_model_(path):
    """Extract skills from model, TEST FUNCTION."""
    files = listdir(path)
    skills = []
    for file in files:
        try:
            html = open_html_file(f"{path}/{file}")
            listing_data = parse_listing_data(html)
            job_details = extract_job_details(html, listing_data)
            job_desc = parse_job_description(listing_data)
            skills.append(extract_skills_from_description(job_desc))
        except:
            print("Error processing:", file)
            continue
    return skills


def get_listing_data(path, file) -> dict:
    try:
        html = open_html_file(f"{path}/{file}")
        listing_data = parse_listing_data(html)
        job_details = extract_job_details(html, listing_data)
        company_details = extract_company_details(listing_data)
        job_desc = parse_job_description(listing_data)
        skills = extract_skills_from_description(job_desc)
    except:
        return f"Error processing: {file}"
    return {'company': company_details, 'job': job_details, 'skills': skills}


if __name__ == "__main__":
    load_dotenv()
    NLP_LG = spacy.load('en_core_web_lg')
    NLP_SKILLS = spacy.load("output/model-best")
    comp_salary = 'job101304099.html'
    range_salary = 'job101290399.html'
    fixed_salary = 'job101266908.html'
    listing_data = get_listing_data("pipeline/etl", range_salary)
    print(listing_data)
    # skills = testing_model_('practise/data_use_this/london/listing')
    # if skills:
    #     load_json(skills)
