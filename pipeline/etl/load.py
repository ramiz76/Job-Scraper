"""
This module populates the job listing database with the extracted data.
"""
from os import environ
from dotenv import load_dotenv
from psycopg2 import extensions, connect, DatabaseError, extras, errors


def db_connection() -> extensions.connection:
    """
    Establish a connection with the database.
    Returns a psycopg2 database connection object or None if connection fails.
    """
    try:
        return connect(dbname=environ["DATABASE_NAME"],
                       user=environ["DATABASE_USERNAME"],
                       host=environ["DATABASE_ENDPOINT"],
                       password=environ["DATABASE_PASSWORD"],
                       cursor_factory=extras.RealDictCursor)
    except Exception as exc:
        raise DatabaseError("Error connecting to database.") from exc


def load_listing_data(conn):
    """
    Load listing data into the database.
    """
    with conn.cursor() as cur:
        cur.execute("""f""")
    conn.commit()


# def populate_skills_table(conn, type_id: int, skill: str) -> int | None:
#     """Populate skills table with skill if not present and returns skill_id."""
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#                 """INSERT INTO skills (type_id,skill) VALUES (%s,%s) RETURNING skill_id;""",
#                 [type_id, skill])
#             skill_id = cur.fetchone()
#         if skill_id:
#             conn.commit()
#             return skill_id
#     except errors.UniqueViolation: # pylint: disable=no-member
#         print('Duplicate data was not inserted:', skill)
#         conn.rollback()
#     return None


def populate_single_column_dimension_table(conn, table: int, column: str, input: str) -> int | None:
    """
    Populate the single column dimension table with relevant data if 
    not present and return primary key id.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO %s (%s) VALUES (%s) RETURNING %s;""",
                [table, column, input, table + "_id"])
            id = cur.fetchone()
        if id:
            conn.commit()
            return id
    except errors.UniqueViolation:  # pylint: disable=no-member
        print('Duplicate data was not inserted:', table)
        conn.rollback()
    return None


def populate_double_column_dimension_table(conn, table: int, column: str, input: str) -> int | None:
    """
    Populate the double column dimension table with relevant data if 
    not present and return primary key id.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO %s (%s,%s) VALUES (%s,%s) RETURNING %s;""",
                [table, column, input, table + "_id"])
            id = cur.fetchone()
        if id:
            conn.commit()
            return id
    except errors.UniqueViolation:  # pylint: disable=no-member
        print('Duplicate data was not inserted:', table)
        conn.rollback()
    return None


def get_skills_type_id(conn, type_name: list):
    """
    Retrieve type_id from database.
    """
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


# def get_skill_id(conn, skill: list):
#     """
#     Retrieve skill_id from database if present else insert skill data into skills table.
#     """
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#                 """SELECT skill_id FROM skills WHERE skill = (%s);""", [skill])
#             skill_id = cur.fetchone()
#         if not skill_id:
#             type_id = get_skills_type_id(skill[1])
#             skill_id = populate_skills_table(conn, type_id, skill[0])
#             skill_id = skill_id['skill_id']
#         return skill_id
#     except DatabaseError:
#         print('Error retrieving keyword id from database', skill)
#     return None


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
    except errors.UniqueViolation:  # pylint: disable=no-member
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
    except errors.UniqueViolation:  # pylint: disable=no-member
        print('Duplicate data was not inserted:', salary)
        conn.rollback()
    return None


def get_id(conn, identifier, input: str):
    """Retrieve specified id from the corresponding table if present else 
    new data into table."""
    try:
        id_key = identifier+"_id"
        with conn.cursor() as cur:
            cur.execute(
                """SELECT %s FROM %s WHERE %s = (%s);""",
                [id_key, identifier, identifier, input])
            id = cur.fetchone()
        if not id:
            id = populate_salary_table(conn, input)
        return id[id_key]
    except DatabaseError:
        print('Error retrieving primary key id from table', identifier)
    return None


def run_load(conn, file: str, listing_data: dict):
    """Execute loading segment of the pipeline."""
    company = listing_data['company']
    job = listing_data['job']
    skills = listing_data['skills']
    salary = job['salary']
    print(salary)
    # company_id = get_company_id(conn, company)
    # low_salary = get_id(conn, 'salary', salary[0])
    # high_salary = get_id(conn, 'salary', salary[1])


if __name__ == "__main__":
    load_dotenv()
    try:
        # FILE = "job101125668.html"
        pass

        # run_load('placeholder', file.strip('.html'), listing_data)

    finally:
        pass
