"""
This module parses job listing data from the web scraped job listing HTML.
"""

import json
import re
from os import environ, listdir
from datetime import datetime
from transformers import pipeline

from bs4 import BeautifulSoup
import spacy
from rapidfuzz import process, distance, fuzz

DATE = datetime.now().strftime("%y_%m_%d")
NLP_LG = spacy.load('en_core_web_lg')
NLP_SKILLS = spacy.load("ner_training/output/model-best")
RANGE_PATTERN = r'([$£€]?\d+(?:[,.]\d{1,3})*\.?\d{0,2}[kK]?)(\s*(?:-|to)\s*([$£€]?\d+(?:[,.]\d{1,3})*\.?\d{0,2}[kK]?))?'


def open_html_file(file_path: str) -> BeautifulSoup:
    """Open job listing html file and return as BeautifulSoup Object."""
    with open(file_path) as html_file:
        html = BeautifulSoup(html_file, 'html.parser')
    return html


def parse_listing_data(file: str, html: BeautifulSoup) -> dict:
    """Extract full job listing data and return in JSON format."""
    try:
        listing_data = html.find("script", id="jobPostingSchema")
        if listing_data:
            listing_data = json.loads(listing_data.string)
        else:
            listing_data = html.find("script", type="application/ld+json")
            listing_data = json.loads(listing_data.string)
    except AttributeError as err:
        print(f"Error extracting listing data ({file}): {err}")
        listing_data = None
    return listing_data


def create_key_pairs(data: dict, key: str) -> str:
    """Pass in keys to extract its value pair from job listings dict."""
    try:
        return data.get(key)
    except (KeyError, AttributeError):
        return None


def extract_job_location(data: dict):
    """Extract location of job listing from varied dictionary reference."""
    try:
        with open("pipeline/cities.txt") as f:
            cities = f.read().splitlines()
        location_one = data.get('jobLocation', {}).get(
            'address', {}).get('addressLocality')
        location_two = data.get('jobLocation', {}).get(
            'address', {}).get('addressRegion')
        if location_one:
            match_one = process.extractOne(location_one.lower(), cities,
                                           scorer=fuzz.token_sort_ratio, score_cutoff=90)
            if match_one:
                return match_one[0].title()
        if location_two:
            match_two = process.extractOne(location_two.lower(), cities,
                                           scorer=fuzz.token_sort_ratio, score_cutoff=90)
            if match_two:
                return match_two[0].title()
    except (KeyError, AttributeError):
        return
    return location_one.title() if location_one else location_two.title() if location_two else None


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
    url_title = get_title_from_url(job_details.get('url'))
    job_details['title_category'] = group_titles_by_category(url_title,
                                                             job_details.get("title"))
    return job_details


def clean_salary_number(salary_number, has_k):
    num = re.sub(r'[k£$€,]', '', salary_number, flags=re.IGNORECASE)
    try:
        if has_k:
            return str(float(num) * 1000)
        return str(float(num))
    except TypeError:
        return None


def find_salary_range(salary_text):
    salary_match = re.search(RANGE_PATTERN, salary_text)
    if salary_match:
        return salary_match.group(0)
    return None


def extract_floats_from_salary(salary_text):
    salary_string = find_salary_range(salary_text)
    if not salary_string:
        return None
    has_k = 'k' in salary_string.lower()
    salary_range = split_salary_range(salary_string)
    cleaned_salary_range = [clean_salary_number(
        salary, has_k) for salary in salary_range]
    return cleaned_salary_range


def split_salary_range(salary_string):
    salary_range = re.split(r'\s*-\s*|\s+to\s+', salary_string)
    return salary_range


def extract_salary_html(html: BeautifulSoup) -> str:
    """Extract job salary text from salary html tag."""
    try:
        salary_html = html.find('section', class_='job-summary')
        if salary_html:
            salary_text = salary_html.find(
                'li', class_='salary icon').get_text()
        else:
            salary_html = html.find('li', class_='job-ad-display-28m62z')
            salary_text = salary_html.find(
                'span', class_='job-ad-display-ys9ncr').get_text()
        return salary_text.lower()
    except AttributeError:
        return None


def extract_job_salary(html: BeautifulSoup) -> dict:
    """Extract the salary range and type from the job listing."""
    salary_text = extract_salary_html(html)
    if not salary_text:
        return {'lower': None, 'upper': None, 'salary_type': 'unspecified'}
    if 'competitive' in salary_text:
        return {'lower': None, 'upper': None, 'salary_type': 'competitive'}
    salary_numbers = extract_floats_from_salary(salary_text)
    if not salary_numbers:
        return {'lower': None, 'upper': None, 'salary_type': 'unspecified'}

    lower = min(salary_numbers)
    upper = max(salary_numbers)
    salary_type = extract_salary_type(lower, upper, salary_text)

    return {'lower': lower, 'upper': upper, 'salary_type': salary_type}


def extract_salary_type(lower, upper, salary_text: str) -> str:
    """Determine the type of salary (annual, monthly, hourly)."""
    if lower and float(lower) > 10000 and upper and float(upper) > 10000:
        return 'year'
    if any(word in salary_text for word in ['year', 'annum', 'annual', 'p.a']):
        return 'year'
    elif any(word in salary_text for word in ['month', 'monthly']):
        return 'month'
    elif any(word in salary_text for word in ['hour', 'hourly']):
        return 'hour'
    elif any(word in salary_text for word in ['day', 'daily']) and not re.search(r'\b\d+\s+days\b', salary_text):
        return 'day'
    return 'unspecified'


def extract_company_details(data: dict) -> dict:
    """Extract hiring company key details."""
    try:
        hiring_org = data.get('hiringOrganization')
        hiring_company = {'company': hiring_org.get('name'),
                          'type': hiring_org.get('@type'),
                          'url': hiring_org.get('url')}
    except (KeyError, AttributeError):
        return {'company': None,
                'type': None,
                'url': None}
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
            tags_list.append([ent.text.replace('\u00a0', ""), ent.label_])
        all_sentence_list.append([sentence.text, {"entities": tags_list}])
    return all_sentence_list


def load_json(skills):
    with open(f'model-output/{DATE}-model_output.json', 'w') as json_file:
        json.dump(skills, json_file, indent=4)


# def testing_model_(path):
#     """Extract skills from model, TEST FUNCTION."""
#     files = listdir(path)
#     skills = []
#     for file in files:
#         try:
#             html = open_html_file(f"{path}/{file}")
#             listing_data = parse_listing_data(html)
#             job_details = extract_job_details(html, listing_data)
#             job_desc = parse_job_description(listing_data)
#             skills.extend(extract_skills_from_description(job_desc))
#         except:
#             print("Error processing:", file)
#             continue
#     return skills


def get_listing_data(path, file) -> dict:
    html = open_html_file(f"{path}/{file}")
    listing_data = parse_listing_data(file, html)
    job_details = extract_job_details(html, listing_data)
    company_details = extract_company_details(listing_data)
    job_desc = parse_job_description(listing_data)
    requirements = extract_skills_from_description(job_desc)
    return {'company': company_details, 'job': job_details, 'requirements': requirements}


def find_most_similar_keyword(single_value: str, keywords: list) -> int:
    keywords_list = [keyword[1].lower()
                     for keyword in keywords if isinstance(keyword[1], str)]
    keywords_dict = {}
    for keyword in keywords:
        keywords_dict[keyword[1].lower()] = keyword[0]
    match = process.extractOne(single_value, keywords_list,
                               scorer=distance.Levenshtein.normalized_similarity, score_cutoff=0.8)
    if match:
        return keywords_dict.get(match[0])
    return None


TITLE_GROUPS = {
    "Data Engineer": ["data engineer", "etl developer", "data engineering", "big data engineer", "data pipeline engineer", "backend"],
    "Software Engineer": ["software engineer", "ux/ui designer", "servicenow developer", ".net developer", "software developer",
                          "application developer", "front end", "web engineer", "frontend engineer", "programmer", "python developer", "java developer", "java engineer", "python engineer", "c# developer", "mobile systems engineer", "full stack"],
    "Cloud Engineer": ["cloud engineer", "cloud consultant", "cloud developer", "cloud integration"],
    "Business Intelligence": ["bi developer", "powerbi developer", "tableau developer", "business intelligence", "bi engineer"],
    "Database Administrator": ["database administrator", "database admin", "sql dba", "sql developer", "mysql dba", "postgresql dba", "database developer", "oracle dba", "sql server dba"],
    "DevOps Engineer": ["devops", "devops engineer", "reliability engineer", "ci/cd engineer", "kubernetes engineer", "docker engineer"],
    "Data Scientist": ["scientist", "data scientist", "machine learning engineer", "ai engineer", "statistical analyst", "data science"],
    "Analyst": ["analyst", "data analyst", "business analyst", "analytics engineer", "technical analyst", "market analyst", "financial analyst"],
    "Architect": ["architect", "solution architect", "technical architect", "data architect", "enterprise architect", "cloud architect"]
}


def get_title_from_url(url: str):
    url_title = re.search(r'job\/([^\/]+)', url)
    if url_title:
        url_title = re.sub(r'-', ' ', url_title.group(1))
        return url_title


def group_titles_by_category(url_title: str, title: str):
    category = "Other"
    title = title.lower()
    title_score = 0
    url_score = 0
    partial_score = 0
    best_partial = ""
    best_url = ""
    l_categories = [title.lower() for title in TITLE_GROUPS.keys()]
    partial_match = process.extractOne(
        title, l_categories, scorer=fuzz.partial_ratio)

    for title_category, keywords in TITLE_GROUPS.items():
        title_match = process.extractOne(
            title, keywords, scorer=fuzz.token_set_ratio)

        url_title_match = process.extractOne(
            url_title, keywords, scorer=fuzz.token_set_ratio)

        if title_match[1] > title_score and title_match[1] > 90:
            title_score = title_match[1]
            category = title_category

        if url_title_match[1] > url_score and url_title_match[1] > 90:
            url_score = url_title_match[1]
            best_url = title_category
    if partial_match and partial_match[1] > 90:
        for partial_category in TITLE_GROUPS.keys():
            if partial_category.lower() == partial_match[0]:
                best_partial = partial_category
    if category == "Other":
        if best_url:
            return best_url
        if best_partial:
            return best_partial
    return category


if __name__ == "__main__":
    salary_text = "70 - 75K + 6% Pension, Private health 25 days etc"
    found = re.search(r'\b\d+\s+days\b', salary_text)
    print(found)
