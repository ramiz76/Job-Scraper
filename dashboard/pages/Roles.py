import streamlit as st
import pandas as pd

from utils import select_listing_data, group_titles, select_titles
from queries import title_groups


def display_grouped_titles():
    """Currently set for Data Engineer roles"""
    titles = select_titles()
    grouped_titles = group_titles(titles.get(
        "rows"), title_groups).get("Data Engineer")
    df = pd.DataFrame(
        {'Experience Level': grouped_titles.keys(),
         'Titles': grouped_titles.values()})
    return df.explode('Titles')


def display_title_level_list(LEVELS):
    """Multiselect option to display job titles by experience level."""
    LEVELS = set(LEVELS)
    choices = st.sidebar.multiselect(
        label="Select Experience Level", options=LEVELS, key='level_choices')
    return choices if choices else LEVELS


if __name__ == "__main__":
    listing_data = select_listing_data()
    titles_df = display_grouped_titles()
    level_choices = display_title_level_list(
        titles_df['Experience Level'].to_list())

    left_column, middle_column, right_column = st.columns([3, 1, 1])

    st.dataframe(
        titles_df.query("`Experience Level` in @level_choices"))
