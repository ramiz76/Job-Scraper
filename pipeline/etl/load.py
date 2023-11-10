
from os import environ
from dotenv import load_dotenv
from psycopg2 import extensions, connect, DatabaseError, extras, errors

from pipeline.etl.transform import get_listing_data


def db_connection() -> extensions.connection | None:
    """Establish connection with the media-sentiment RDS"""
    try:
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_ENDPOINT"],
                       password=environ["DATABASE_PASSWORD"],
                       cursor_factory=extras.RealDictCursor)

    except Exception as exc:
        raise DatabaseError("Error connecting to database.") from exc


def load_listing_data(conn):
    with conn.cursor() as cur:
        cur.execute("""f""")
    conn.commit()


def populate_skills_table(conn, type_id: int, skill: str) -> int | None:
    """Populate skills table with skill if not present and returns skill_id."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO skills (type_id,skill) VALUES (%s,%s) RETURNING skill_id;""",
                [type_id, skill])
            skill_id = cur.fetchone()
        if skill_id:
            conn.commit()
            return skill_id
    except errors.UniqueViolation:
        print('Duplicate data was not inserted:', skill)
        conn.rollback()
    return None


def get_skills_type_id(conn, type_name: list):
    """Retrieve type_id from database."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT type_id FROM skills_type WHERE type_name = (%s);""",
                [type_name])
            type_id = cur.fetchone()
            return type_id
    except DatabaseError:
        print('Error retrieving keyword id from database', type_name)
    return None


def get_skill_id(conn, skill: list):
    """Retrieve skill_id from database if present else insert skill data into skills table."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT skill_id FROM skills WHERE skill = (%s);""", [skill])
            skill_id = cur.fetchone()
        if not skill_id:
            type_id = get_skills_type_id(skill[1])
            skill_id = populate_skills_table(conn, type_id, skill[0])
            skill_id = skill_id['skill_id']
        return skill_id
    except DatabaseError:
        print('Error retrieving keyword id from database', skill)
    return None


def populate_company_table(conn, company: dict):
    """Populate company table with company data if not present and returns company_id."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO company (company_name,company_type,company_url) 
                VALUES (%s,%s,%s) RETURNING company_id;""",
                [company['name'], company['type'], company['url']])
            company_id = cur.fetchone()
        if company_id:
            conn.commit()
            return company_id
    except errors.UniqueViolation:
        print('Duplicate data was not inserted:', company['name'])
        conn.rollback()
    return None


def get_company_id(conn, company: dict):
    """Retrieve company id from the database if present else insert 
    company data into company table."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT company_id FROM company WHERE company_name = (%s);""",
                [company['name']])
            company_id = cur.fetchone()
        if not company_id:
            company_id = populate_company_table(conn, company)
            company_id = company_id['company_id']
        return company_id
    except DatabaseError:
        print('Error retrieving company_id from database', company['name'])
    return None


def populate_salary_table(conn, salary: str) -> dict:
    """Populate salary table with salary data if not present and returns salary_id."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO salary (salary_value) VALUES (%s) 
                RETURNING salary_id;""",
                [salary])
            salary_id = cur.fetchone()
        if salary_id:
            conn.commit()
            return salary_id
    except errors.UniqueViolation:
        print('Duplicate data was not inserted:', salary)
        conn.rollback()
    return None


def get_salary_id(conn, salary: str):
    """Retrieve salary id from the database if present else 
    insert salary data into salary table."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT salary_id FROM salary WHERE salary_value = (%s);""",
                [salary])
            salary_id = cur.fetchone()
        if not salary_id:
            salary_id = populate_salary_table(conn, salary)
            salary_id = salary_id['salary_id']
        return salary_id
    except DatabaseError:
        print('Error retrieving company_id from database', salary)
    return None


def run_load(conn, file: str, listing_data: dict):
    """Execute loading segment of the pipeline."""
    company = listing_data['company']
    job = listing_data['job']
    skills = listing_data['skills']
    salary = job['salary']

    company_id = get_company_id(conn, company)
    low_salary = get_salary_id(conn, salary[0])
    high_salary = get_salary_id(conn, salary[1])

    print(company)
    # for sentence, skills_list in skills.items():
    #     for skill in skills_list:
    #         get_skill_id(conn, skill)
    #         load_listing_data(conn, job)


if __name__ == "__main__":
    load_dotenv()
    try:
        # connection = db_connection()
        # path = "../practise/data_use_this/bristol/listing"
        file = "job101125668.html"
        # html = open_html_file(
        #     "../practise/data_use_this/bristol/listing/job101125668.html")
        # listing_data = parse_listing_data(html)
        # job_details = extract_job_details(html, listing_data)
        # company_details = extract_company_details(listing_data)
        # job_desc = parse_job_description(listing_data)
        # skills = extract_skills_from_description(job_desc)
        # listing_data = get_listing_data(path, file)
        listing_data = {'company': {'name': 'CGI', 'company_type': 'Organization', 'url': 'https://www.totaljobs.com/jobs-at/cgi-group/jobs'}, 'job': {'title': 'Data Engineer', 'url': 'https://www.totaljobs.com/job/data-engineer/cgi-job101125668', 'date': '2023-09-08T13:59+01:00', 'industry': 'IT, IT-Database', 'employment_type': ['FULL_TIME'], 'city': 'Chippenham, Wiltshire', 'salary': 'competitive'}, 'skills': {'Design, implementation, and management of data processing pipelines': [['data processing', 'SOFT']], 'Management of Data Warehousing and Data Marts.': [['Data Warehousing', 'SOFT']], 'Monitoring and assurance of data lifecycle management processes': [['data lifecycle', 'SOFT']], 'Identification and reporting of performance optimisations': [['Identification', 'SOFT']], 'Production of Data Design documents': [], 'Good interpersonal skills and able to communicate with the varying stakeholders.': [
        ], 'Comprehensive working knowledge and experience of data warehousing and data processing (ETL).': [['data warehousing', 'SOFT'], ['data processing', 'SOFT'], ['ETL', 'SOFT']], 'Comprehensive working knowledge and experience of Big Data Solutions namely Hadoop or Splunk.': [['Big Data Solutions', 'SOFT'], ['Hadoop', 'HARD'], ['Splunk', 'HARD']], 'Understanding of data connectivity to visualisation tools': [['data connectivity', 'SOFT'], ['visualisation', 'SOFT']], 'Understanding of computer networking (WAN), including network design, security, and logging.': [], 'Experience of open-source data processing/management tools': [], 'Experience of working with network security data sets, such as Syslog': [['network security', 'SOFT'], ['Syslog', 'HARD']], 'Familiarity with Red Hat Linux Operating System.': [['Red', 'HARD'], ['Linux Operating System.', 'CERT']], 'Ability to write scripts using Python or Bash.': [['write', 'SOFT'], ['Python', 'HARD'], ['Bash', 'HARD']]}}
        run_load('placeholder', file.strip('.html'), listing_data)

    finally:
        # connection.close()
        pass