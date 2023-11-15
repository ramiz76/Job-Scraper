# Job Scraper

## Overview
Job Scraper is a Python based tool designed to scrape 'Data Engineer' job listings from various major cities in the UK. With the use of string manipulation techniques and a custom built SpaCy NER (Named Entity Recognition) model, this project aims to gather a range of job listing details, including job titles, company information, salary, and specific skills, certifications, and perks mentioned. <br/>
With this project, I intend to explore the job market landscape by answering questions, such as:

- What skills are currently most valued in major cities?
- How do specific skills impact salary levels?
- Is there a correlation between the posting date of a job and its salary range?
- Do particular cities offer more competitive perks?

## Features
- Web scraping job listings from specified URLs.
- Extracting key job information such as job title, company, salary, etc.
- Custom NER model to identify and extract specific entities such as skills, certifications, and perks.
- Storage of data in a relational database.

## Technologies
- Python
- BeautifulSoup
- Selenium
- SpaCy
- PostgreSQL

## Setup
1. Clone this repository.
2. Activate a new virtual environment.
3. Run `pip3 install -r requirements.txt`
4. Run `python3 -m spacy download en_core_web_lg` 
5. Create .env file, containing the following environment variables:
```
DATABASE_NAME=<db name>
DATABASE_USERNAME=<your username>
DATABASE_ENDPOINT=localhost | <AWS RDS endpoint address>
DATABASE_PASSWORD=XXXXXXXXXXX
ACCESS_KEY_ID=XXXXXXXXXXX
SECRET_ACCESS_KEY=XXXXXXXXXXX
```

## Architecture Diagram


## Acknowledgements
- This project uses data from [TotalJobs](https://www.totaljobs.com/).
- NER model training powered by SpaCy.

