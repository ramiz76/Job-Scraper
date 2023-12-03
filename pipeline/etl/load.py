"""
This module populates the job listing database with the extracted data.
"""
from os import environ

from dotenv import load_dotenv
from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from psycopg2.errors import UniqueViolation
from psycopg2.sql import Identifier, SQL, Placeholder, Literal

from transform import find_most_similar_keyword

LISTING_NAMES = [
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
        load_dotenv()
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_HOST"],
                       password=environ["DATABASE_PASSWORD"]
                       )
    except Exception as exc:
        raise DatabaseError("Error connecting to database.") from exc


def populate_table(conn, table_name, column_names: list, data: list) -> int:
    """
    Populate the table with relevant data if 
    not present and return primary key id.
    """
    try:
        if isinstance(data[0], dict):
            column_names = list(data[0].keys())
            data = list(data[0].values())
        with conn.cursor() as cur:
            columns = SQL(', ').join(map(Identifier, column_names))
            values = SQL(', ').join(Placeholder() * len(data))
            query = SQL(
                """INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING {id};""").format(
                table=Identifier(table_name),
                columns=columns,
                values=values,
                id=Identifier(table_name + "_id"))
            cur.execute(query, data)
            id = cur.fetchone()
            if id:
                conn.commit()
                return id[0]
    except UniqueViolation:
        # print(f'Duplicate data was not inserted: {table_name} table')
        conn.rollback()
    return None


def get_id(conn, table_name: str, data: list, column_names=""):
    """
    Retrieve id from database.
    """
    try:
        column_names = [table_name] if not column_names else column_names
        if isinstance(data[0], dict):
            single_value = data[0].get(column_names[0])
        else:
            single_value = data[0]
        with conn.cursor() as cur:
            query = SQL(
                """SELECT {id} FROM {table} WHERE {column} = %s;""")
            formatted_query = query.format(
                id=Identifier(table_name + "_id"),
                table=Identifier(table_name),
                column=Identifier(column_names[0])
            )
            cur.execute(formatted_query, [single_value])
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                if table_name == 'requirement':
                    similar_keywords = find_similar_keyword(
                        conn, ['requirement_id', 'alias'], 'alias', single_value)
                    if similar_keywords:
                        match = find_most_similar_keyword(
                            single_value, similar_keywords)
                        if match:
                            return match
                return populate_table(conn, table_name, column_names, data)

    except DatabaseError as err:
        print(f'Error retrieving ID from database for {table_name} : {err}')
        return None


def find_similar_keyword(conn, column_names, table, keyword):
    """Query database to return data that are similar to keyword"""
    try:
        columns = SQL(', ').join(map(Identifier, column_names))
        with conn.cursor() as cur:
            query = SQL("SELECT {column} FROM {table} WHERE {table} ILIKE {keyword} ESCAPE ''").format(
                table=Identifier(table),
                column=columns,
                keyword=Literal("%" + keyword + "%")
            )
            cur.execute(query)
            result = cur.fetchall()
        if result:
            return result
    except (IndexError, TypeError) as e:
        print(f"Error during search: {e}")
        return None


def run_load(conn, file: str, listing_data: dict):
    """Execute loading segment of the pipeline."""
    company = listing_data['company']
    job = listing_data['job']
    requirements = listing_data['requirements']
    salary = job['salary']
    salary[2] = 'unspecified' if salary[2] is None else salary[2]
    low_salary_id = get_id(conn, table_name='salary', data=[salary[0]])
    high_salary_id = get_id(conn, table_name='salary',
                            data=[salary[1]])
    location_id = get_id(conn, table_name='location',
                         data=[job.get("location")])
    title_id = get_id(conn, table_name='title',
                      data=[job.get("title")])
    posting_date_id = get_id(
        conn, table_name='posting_date', data=[job.get("date")])
    company_id = get_id(conn, table_name='company', data=[company])
    salary_type_id = get_id(
        conn, table_name='salary_type', data=[salary[2]])
    employment_type_id = get_id(
        conn, table_name='employment_type', data=[job.get("employment_type")[0]])
    industry_id = get_id(conn, table_name='industry',
                         data=[job.get("industry")])
    listing_data = [file, job.get("url"), title_id, low_salary_id, high_salary_id, location_id, posting_date_id,
                    company_id, salary_type_id, employment_type_id, industry_id]

    job_listing_id = populate_table(
        conn, table_name=LISTING_NAMES[0], column_names=LISTING_NAMES, data=listing_data)
    if job_listing_id:
        for requirement in requirements:
            entities = requirement[1].get("entities")
            for entity in entities:
                keyword = entity[0]
                requirement_type_id = get_id(conn, table_name='requirement_type',
                                             data=[entity[1]])
                requirement_id = get_id(conn, table_name='requirement',
                                        column_names=['requirement',
                                                      'requirement_type_id'],
                                        data=[keyword.lower(), requirement_type_id])
                populate_table(conn, table_name='requirement_link', column_names=[
                    'requirement_id', 'job_listing_id'], data=[requirement_id, job_listing_id])

