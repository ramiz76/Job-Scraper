from os import environ
from collections import defaultdict
import re

from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from psycopg2.sql import SQL
from dotenv import load_dotenv
import streamlit as st

from queries import title_groups, top_requirements, all_requirements, listing_data, all_titles, grouped_requirements, all_requirement_links, all_aliases, listing_count


def get_requirement_data():
    pass


def centre_text(size, text, color='white', weight='normal'):
    return f"""<div style='text-align: center; color: {color}; 
    font-weight: {weight}; font-size: {size}px;'>{text}</div>"""


def db_connection():
    """
    Establish a connection with the database using Streamlit's connection management.
    """
    load_dotenv()
    try:
        conn = connect(
            dbname=environ["DATABASE_NAME"],
            user=environ["DATABASE_USERNAME"],
            host=environ["DATABASE_HOST"],
            password=environ["DATABASE_PASSWORD"])
        return conn
    except DatabaseError as err:
        print(f"Error connecting to database: {err}")
        return None


# @st.cache_data
def select_requirement_links():
    """Get all requirements from database"""
    conn = db_connection()
    return execute(conn, all_requirement_links)


# @st.cache_data
def select_top_requirements(n=10):
    """GET top N number of requirements from database"""
    conn = db_connection()
    return execute(conn, SQL(top_requirements))


def select_grouped_requirements():
    """GET grouped requirements and listing count from database"""
    conn = db_connection()
    return execute(conn, SQL(grouped_requirements))


# @st.cache_data
def select_listing_data():
    conn = db_connection()
    return execute(conn, listing_data)


def select_listing_count():
    conn = db_connection()
    return execute(conn, listing_count)


# @st.cache_data
def select_titles():
    conn = db_connection()
    return execute(conn, all_titles)

# @st.cache_data


def select_alias():
    conn = db_connection()
    return execute(conn, all_aliases)


# @st.cache_resource
def execute(_conn, _query):
    """Execute query blueprint"""
    try:
        with _conn.cursor() as cur:
            cur.execute(_query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
        return {"columns": columns, "rows": rows}
    except (AttributeError, DatabaseError) as err:
        print(f"Error querying database: {err}")
        return None
    finally:
        _conn.close()


def group_titles(row):
    title = row["title"]
    l_title = title.lower()
    found_category = False
    level = find_title_level(l_title)
    for title_group in title_groups.keys():
        if title_group.lower() in l_title:
            found_category = title_group
            break
    if not found_category:
        for title_group, keywords in title_groups.items():
            if any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b',
                             l_title) for keyword in keywords):
                found_category = title_group
                break
    if found_category:
        row["title_category"] = found_category
    else:
        row["title_category"] = "Other"
    row["title_level"] = level
    return row


def find_title_level(title):
    """Finds experience level in job title."""
    level = "Mid Level"
    if any(word in title for word in ["senior", "lead", "principal", "head", "manager"]):
        level = "Senior Level"
    elif any(word in title for word in ["junior", "graduate", "apprentice", "intern", "early careers"]):
        level = "Junior Level"
    return level
