import json

from bs4 import BeautifulSoup
import spacy

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


def open_html_file() -> str:
    """Retrieve HTML data from file and returns as BeautifulSoup object."""
    file = "london/listing/job101187548.html"
    file_two = "london/listing/job101266908.html"
    with open(file_two) as html_file:
        html = BeautifulSoup(html_file, 'html.parser')
    return html


def parse_company_data(html: str) -> str:
    """Extract data from listings full job description webpage"""
    data = (html.find("script", id="jobPostingSchema")).string
    data = json.loads(data)
    return data


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

def extract_job_description(data: str):
    desc = data.get('description')
    desc = BeautifulSoup(desc, 'html.parser')
    all_text = desc.get_text()
    # print(all_text)

    p_elements = desc.find_all('p')
    p_texts = [p.text for p in p_elements]

    li_elements = desc.find_all('li')
    listed_text = [li.text for li in li_elements]

    return [p_texts, listed_text]


def extract_relevant_text(text: list, listed_text: list):
    nlp_text = nlp(listed_text)
    tokens = [token.text for token in nlp_text if not token.is_stop]


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_lg")
    html = open_html_file()
    data = parse_company_data(html)
    desc = extract_job_description(data)
    extract_relevant_text(desc[0], desc[1])
