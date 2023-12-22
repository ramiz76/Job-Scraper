import streamlit as st
import pandas as pd

from utils import select_requirement_links, select_alias, select_grouped_requirements
from static import home_set_left_column
CHOICES = ('HARD', 'SOFT', 'PERK', 'CERT')
GENERAL_SKILLS = ['SQL']


def display_requirement_list():
    """Multiselect option to display requirement count by requirement type."""
    choices = st.sidebar.multiselect(
        label="Select Requirement Type", options=CHOICES, key='type_choices')
    return choices if choices else CHOICES


def set_type_df(response):
    df = pd.DataFrame(columns=response['columns'], data=response['rows'])
    # df.to_csv('dashboard/requirements.csv', index=False)
    return df[['Requirement', 'Requirement Type', 'Listing Count', 'Total Listings']]


def create_dataframe(response, chosen_columns=""):
    if not chosen_columns:
        chosen_columns = response['columns']
    return pd.DataFrame(columns=chosen_columns, data=response['rows'])


def group_skills(req_df):
    """Create groupings for skill keywords."""
    grouped_req_df = req_df.groupby('Requirement').agg(
        {'Requirement': 'first', 'Listing ID': 'count',
         'Requirement Type': 'first'})
    grouped_req_df.rename(
        columns={"Listing ID": "Listing Count"}, inplace=True)
    return grouped_req_df.sort_values('Listing Count', ascending=False)


def replace_requirement(row):
    matching_ids = aliases_df[aliases_df['Alias'].str.lower(
    ) == row['Requirement'].lower()]['Requirement ID']
    if not matching_ids.empty:
        requirement_id = matching_ids.iloc[0]
        return id_to_requirement.get(requirement_id, row['Requirement'])
    return row['Requirement']


def group_aliases(req_df):
    req_df['Requirement'] = req_df.apply(replace_requirement, axis=1)
    return group_skills(req_df)


def get_grouped_requirements():
    response = select_grouped_requirements()
    return pd.DataFrame(columns=response['columns'], data=response['rows'])


def get_skill_details(skill, skill_id):
    """Return DataFrame with details associated with skill."""


if __name__ == "__main__":
    all_requirements = select_requirement_links()
    grouped_requirements = get_grouped_requirements()
    aliases = select_alias()
    aliases_df = create_dataframe(aliases)
    req_df = create_dataframe(all_requirements)

    id_to_requirement = req_df.set_index('Requirement ID')[
        'Requirement'].to_dict()
    req_df = group_aliases(req_df)
    type_choices = display_requirement_list()
    left_column, middle_column, right_column = st.columns([3, 1, 1])
    with left_column:
        home_set_left_column(req_df, type_choices, "Requirement Type")
