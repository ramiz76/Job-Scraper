import json

from bs4 import BeautifulSoup
import spacy
from dotenv import load_dotenv
from spacy.matcher import PhraseMatcher
from spaczz.matcher import FuzzyMatcher


# To extract:
# Job posted date (if recently then todays date)
# job title
# job location (address and postcode)
# salary if available
# company
# job type (permanent, work from home, contract etc)
# what the role will have you do
# what skills are required
# benefits provided


def open_html_file() -> BeautifulSoup:
    """Retrieve HTML data from file and returns as BeautifulSoup object."""
    file = "london/listing/job101187548.html"
    file_two = "london/listing/job101266908.html"
    with open(file) as html_file:
        html = BeautifulSoup(html_file, 'html.parser')
    return html


def parse_company_data(html: BeautifulSoup) -> str:
    """Extract data from listings full job description webpage"""
    company_data = (html.find("script", id="jobPostingSchema")).string
    company_data = json.loads(company_data)
    return company_data


def extract_company_data(data: str):
    """Extract data from listings full job description webpage"""
    title = data.get('title')
    url = data.get('url')
    date = data.get('datePosted')
    industry = data.get('industry')
    employment_type = data.get('employmentType')
    hiring_company_name = data.get('hiringOrganization').get('name')
    hiring_company_type = data.get('hiringOrganization').get('@type')
    hiring_company_url = data.get('hiringOrganization').get('url')
    city = data.get('jobLocation').get('address').get('addressLocality')
    if not city:
        city = data.get('jobLocation').get('address').get('addressRegion')
    salary = (html.find('li', class_='salary')).find(
        'div').get_text()


# if a <li> is located in the description then it has bullet points to state either requirements, responsibilities or benefits
# may not be all of them
# if not located then it will be bundled together within the <p> tags

def extract_job_description(data: str) -> list:
    """make this two functions"""
    desc = data.get('description')
    desc = BeautifulSoup(desc, 'html.parser')

    p_elements = desc.find_all('p')
    p_texts = [p.text for p in p_elements]

    li_elements = desc.find_all('li')
    listed_desc = [li.text for li in li_elements]

    return listed_desc


def open_skills_json() -> set:
    """Retrieve all skill names stored in json file as a set."""
    with open('skills.json', 'r') as skills_json:
        data = json.load(skills_json)
    skills_set = set(data.keys())
    return skills_set


def extract_skills_from_description(listed_desc: list):
    skills_list = []
    for sentence in nlp.pipe(listed_desc, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):

        matched_skills = skill_matcher(sentence)
        for skill_dec in matched_skills:
            skill = sentence[skill_dec[1]:skill_dec[2]]
            skills_list.append(skill.text)
    return skills_list


if __name__ == "__main__":
    load_dotenv()
    nlp = spacy.load("en_core_web_lg")
    skills_set = open_skills_json()
    # skill_matcher = FuzzyMatcher(nlp.vocab)
    skill_matcher = PhraseMatcher(nlp.vocab)
    patterns = set(nlp(text) for text in skills_set)
    skill_matcher.add('SKILLS', None, *patterns)

    html = open_html_file()
    company_data = parse_company_data(html)
    listed_desc = extract_job_description(company_data)
    print(extract_skills_from_description(listed_desc))
