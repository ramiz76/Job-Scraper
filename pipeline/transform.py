import json

from bs4 import BeautifulSoup

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
    with open('../london/listing/job101124321.html') as html_file:
        html = BeautifulSoup(html_file, 'html.parser')
    return html


def get_listing_data(html):
    """Extract data from listings full job description webpage"""
    data = (html.find("script", id="jobPostingSchema")).string
    data = json.loads(data)
    title = data.get('title')
    url = data.get('url')
    date = data.get('datePosted')
    industry = data.get('industry')
    employment_type = data.get('employmentType')
    hiring_company_name = data.get('hiringOrganization').get('name')
    hiring_company_type = data.get('hiringOrganization').get('@type')
    hiring_company_url = data.get('hiringOrganization').get('url')
    city = data.get('jobLocation').get('address').get('addressLocality')
    salary = (html.find('li', class_='salary')).find(
        'div').get_text()

    desc = data.get('description')

    print(city)


if __name__ == "__main__":
    html = open_html_file()
    get_listing_data(html)
