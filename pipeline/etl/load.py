"""
This module populates the job listing database with the extracted data.
"""
from os import environ
from dotenv import load_dotenv
from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from psycopg2.errors import UniqueViolation
from psycopg2.sql import Identifier, SQL, Placeholder

LISTING_NAMES = variable_names = [
    "job_listing",
    "url",
    "title_id",
    "low_salary_id",
    "high_salary_id",
    "location_id",
    "posting_date_id",
    "company_id",
    "salary_type_id",
    "employment_type_id",
    "industry_id"
]


def db_connection() -> connection:
    """
    Establish a connection with the database.
    Returns a psycopg2 database connection object or None if connection fails.
    """
    try:
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_HOST"],
                       password=environ["DATABASE_PASSWORD"]
                       )
    except Exception as exc:
        raise DatabaseError("Error connecting to database.") from exc


def populate_table(conn, names: list, data: str | dict) -> int:
    """
    Populate the table with relevant data if 
    not present and return primary key id.
    """
    try:
        if isinstance(data[0], dict):
            names = list(data[0].keys())
            data = list(data[0].values())
        with conn.cursor() as cur:
            columns = SQL(', ').join(map(Identifier, names))
            values = SQL(', ').join(Placeholder() * len(data))
            query = SQL(
                """INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING {id};""").format(
                table=Identifier(names[0]),
                columns=columns,
                values=values,
                id=Identifier(names[0] + "_id"))
            cur.execute(query, list(data))
            id = cur.fetchone()
            if id:
                conn.commit()
                return id[0]
    except UniqueViolation:
        print(f'Duplicate data was not inserted: {names[0]}')
        conn.rollback()
    return None


def get_id(conn, name: list, search_value: str | dict):
    """
    Retrieve id from database.
    """
    try:
        if isinstance(search_value, dict):
            single_value = search_value.get(name[0])
        else:
            single_value = search_value
        with conn.cursor() as cur:
            query = SQL(
                """SELECT {id} FROM {table} WHERE {column} = %s;""")
            formatted_query = query.format(
                id=Identifier(name[0] + "_id"),
                table=Identifier(name[0]),
                column=Identifier(name[0])
            )
            cur.execute(formatted_query, [single_value])
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return populate_table(conn, name, [search_value])

    except DatabaseError as err:
        print(f'Error retrieving ID from database for {name[0]} : {err}')
        return None


def run_load(conn, file: str, listing_data: dict):
    """Execute loading segment of the pipeline."""
    company = listing_data['company']
    job = listing_data['job']
    skills = listing_data['skills']  # change this name to requirements
    salary = job['salary']
    low_salary_id = get_id(conn, ['salary'], salary[0])
    high_salary_id = get_id(conn, ['salary'], salary[1])
    location_id = get_id(conn, ["location"], job.get("location"))
    title_id = get_id(conn, ["title"], job.get("title"))
    posting_date_id = get_id(conn, ["posting_date"], job.get("date"))
    company_id = get_id(conn, ["company"], company)
    salary_type_id = get_id(conn, ["salary_type"], salary[2])
    employment_type_id = get_id(
        conn, ["employment_type"], job.get("employment_type")[0])
    industry_id = get_id(conn, ["industry"], job.get("industry"))
    listing_data = [file, job.get("url"), title_id, low_salary_id, high_salary_id, location_id, posting_date_id,
                    company_id, salary_type_id, employment_type_id, industry_id]

    # requirements = [job_id, re]
    populate_table(conn, LISTING_NAMES, listing_data)
    # populate_table(conn)


if __name__ == "__main__":
    load_dotenv()
    listing_data = {'company': {'company': 'CGI', 'company_type': 'Organization',
                                'company_url': 'https://www.totaljobs.com/jobs-at/cgi-group/jobs'}, 'job': {'title': 'Data Engineer', 'url': 'https://www.totaljobs.com/job/data-engineer/cgi-job101125668', 'date': '2023-09-08T13:59+01:00', 'industry': 'IT, IT-Database', 'employment_type': ['FULL_TIME'], 'location': 'Chippenham, Wiltshire', 'salary': [None, None, 'competitive']}, 'skills': {'Design, implementation, and management of data processing pipelines': [['data processing', 'SOFT']], 'Management of Data Warehousing and Data Marts.': [['Data Warehousing', 'SOFT']], 'Monitoring and assurance of data lifecycle management processes': [['data lifecycle', 'SOFT']], 'Identification and reporting of performance optimisations': [['Identification', 'SOFT']], 'Production of Data Design documents': [], 'Good interpersonal skills and able to communicate with the varying stakeholders.': [
                                ], 'Comprehensive working knowledge and experience of data warehousing and data processing (ETL).': [['data warehousing', 'SOFT'], ['data processing', 'SOFT'], ['ETL', 'SOFT']], 'Comprehensive working knowledge and experience of Big Data Solutions namely Hadoop or Splunk.': [['Big Data Solutions', 'SOFT'], ['Hadoop', 'HARD'], ['Splunk', 'HARD']], 'Understanding of data connectivity to visualisation tools': [['data connectivity', 'SOFT'], ['visualisation', 'SOFT']], 'Understanding of computer networking (WAN), including network design, security, and logging.': [], 'Experience of open-source data processing/management tools': [], 'Experience of working with network security data sets, such as Syslog': [['network security', 'SOFT'], ['Syslog', 'HARD']], 'Familiarity with Red Hat Linux Operating System.': [['Red', 'HARD'], ['Linux Operating System.', 'CERT']], 'Ability to write scripts using Python or Bash.': [['write', 'SOFT'], ['Python', 'HARD'], ['Bash', 'HARD']]}}

    new_listing_data = {
        'company': {
            'company': 'Acme Corp',
            'company_type': 'Enterprise',
            'company_url': 'https://www.example.com/jobs-at/acme-corp/jobs'
        },
        'job': {
            'title': 'Software Developer',
            'url': 'https://www.example.com/job/software-developer/acme-job102233344',
            'date': '2023-10-15T10:00+01:00',
            'industry': 'Software Development, IT-Services',
            'employment_type': ['PART_TIME'],
            'location': 'Springfield',
            'salary': [30000, 40000, 'competitive']
        },
        'skills': {
            'Expertise in frontend and backend development': [['Frontend Development', 'HARD'], ['Backend Development', 'HARD']],
            'Proficient in Java and JavaScript programming': [['Java', 'HARD'], ['JavaScript', 'HARD']],
            'Experience in agile methodologies and Scrum': [['Agile Methodologies', 'SOFT'], ['Scrum', 'SOFT']],
            'Familiarity with cloud services like AWS or Azure': [['AWS', 'HARD'], ['Azure', 'HARD']],
            'Strong problem-solving skills and analytical thinking': [],
            'Effective communication and team collaboration skills': [],
            'Experience in database management and SQL': [['Database Management', 'HARD'], ['SQL', 'HARD']],
            'Understanding of DevOps principles and CI/CD pipelines': [['DevOps', 'SOFT'], ['CI/CD Pipelines', 'SOFT']],
            'Knowledge in web technologies such as HTML, CSS, and React': [['HTML', 'HARD'], ['CSS', 'HARD'], ['React', 'HARD']],
            'Ability to adapt to new technologies and frameworks': [],
            'Experience with version control systems like Git': [['Git', 'HARD']],
            'Strong debugging and troubleshooting skills': [],
            'Experience in mobile application development': [['Mobile Application Development', 'HARD']],
            'Familiarity with Linux/Unix environments': [['Linux', 'HARD'], ['Unix', 'HARD']],
            'Proficiency in Python and/or Ruby programming': [['Python', 'HARD'], ['Ruby', 'HARD']]
        }
    }

    try:
        db_conn = db_connection()
        run_load(db_conn, 'job1222345', new_listing_data)

    finally:
        pass
