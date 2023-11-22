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
from rapidfuzz.distance import Levenshtein
from rapidfuzz.process import extractOne, extract

comp_salary = 'job101304099.html'
range_salary = 'job101290399.html'
fixed_salary = 'job101266908.html'

DATE = datetime.now().strftime("%y_%m_%d")
PERIOD = {'year': ['year', 'annum', 'annual', 'annually', 'p.a'],
          'month': ['month', 'monthly'],
          'day': ['day', 'daily'],
          'hour': ['hour', 'hourly']}
NLP_LG = spacy.load('en_core_web_lg')
NLP_SKILLS = spacy.load("ner_training/output/model-best")


# TODO
# Create a link table for employment type where there can be multiple (FULL TIME, INTERN etc)

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
    """Extract location of job listing from varied dictionary reference."""
    try:
        location = (data.get('jobLocation', {}).get('address', {}).get('addressLocality') or
                    data.get('jobLocation', {}).get('address', {}).get('addressRegion'))
    except (KeyError, AttributeError):
        location = None
    return location


def extract_job_details(html, data: dict) -> dict:
    """Extract key details of job listing."""
    job_details = {}
    job_details['title'] = create_key_pairs(data, 'title')
    job_details['url'] = create_key_pairs(data, 'url')
    job_details['date'] = create_key_pairs(data, 'datePosted')
    job_details['industry'] = create_key_pairs(data, 'industry')
    job_details['employment_type'] = create_key_pairs(data, 'employmentType')
    job_details['location'] = extract_job_location(data)
    job_details['salary'] = extract_job_salary(html)
    return job_details


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
        return [None, None, 'unspecified']
    if 'competitive' in salary_text:
        return [None, None, 'competitive']

    money_entities = [ent.text for ent in NLP_LG(
        salary_text).ents if ent.label_ == 'MONEY']
    ranges = find_numbers_from_salary_text(money_entities)
    period = extract_salary_type(salary_text)
    salary = find_salary_range(ranges, period)
    if not salary[2] and isinstance(salary[1], int) and salary[1] > 20000:
        salary[2] = 'year'
    return salary


def find_salary_range(ranges: list, period: str) -> list:
    """Return salary range based on extracted numbers."""
    if not ranges:
        return [None, None, 'unspecified']
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
        hiring_company = {'company': hiring_org.get('name'),
                          'type': hiring_org.get('@type'),
                          'url': hiring_org.get('url')}
    except (KeyError, AttributeError):
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


def extract_skills_from_description(job_desc: list) -> list:
    all_sentence_list = []
    for sentence in job_desc:
        tags_list = []
        sentence = NLP_SKILLS(sentence)
        for ent in sentence.ents:
            tags_list.append([ent.text, ent.label_])
        all_sentence_list.append([sentence.text, {"entities": tags_list}])
    return all_sentence_list


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
            skills.extend(extract_skills_from_description(job_desc))
        except:
            print("Error processing:", file)
            continue
    return skills


def get_listing_data(path, file) -> dict:
    html = open_html_file(f"{path}/{file}")
    listing_data = parse_listing_data(html)
    job_details = extract_job_details(html, listing_data)
    company_details = extract_company_details(listing_data)
    job_desc = parse_job_description(listing_data)
    requirements = extract_skills_from_description(job_desc)
    return {'company': company_details, 'job': job_details, 'requirements': requirements}


def find_most_similar_keyword(keyword: str, keywords: list) -> int:
    keywords_list = [keyword[1].lower()
                     for keyword in keywords if isinstance(keyword[1], str)]
    keywords_dict = {}
    for keyword in keywords:
        keywords_dict[keyword[1]] = keyword[0]

    match = extractOne(keyword[1].lower(), keywords_list,
                       scorer=Levenshtein.normalized_similarity, score_cutoff=0.8)
    if match:
        return keywords_dict.get(match)
    return None


if __name__ == "__main__":
    load_dotenv()
    listing = 'job101446543.html'
    listing_two = 'job101446543.html'
    listing_three = 'job101444078.html'
    # listing_data = get_listing_data("manchester/listing", listing_three)
    # print(listing_data)
    # skills = testing_model_('practise/data_use_this/bristol/listing')
    # if skills:
    #     load_json(skills)
