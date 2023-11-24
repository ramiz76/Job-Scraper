
from os import environ
from dotenv import load_dotenv
import json

from load import db_connection, populate_table

REQUIREMENTS = {"HARD": 1, "SOFT": 2, "CERT": 3, "PERK": 4}


def open_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data


def populate_alias_table(conn, data: list):
    for dict in data:
        requirement_type = dict['requirement_type']
        requirement_id = populate_table(conn, 'requirement', ['requirement', 'requirement_type_id'],
                                        [dict["requirement"], REQUIREMENTS[requirement_type]])
        aliases = dict['alias']
        for alias in aliases:
            populate_table(conn, 'alias', [
                'requirement_id', 'alias'], [requirement_id, alias])


if __name__ == "__main__":
    load_dotenv()
    try:
        data = open_json("sandbox/stem_alias_db.json")
        db_connect = db_connection()
        populate_alias_table(db_connect, data)
    finally:
        db_connect.close()
