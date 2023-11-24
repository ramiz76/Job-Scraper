"""Homepage for dashboard"""
from datetime import datetime, date

import streamlit as st
import pandas as pd

from helper_functions import select_top_requirements

CHOICES = ['HARD', 'SOFT', 'PERK', 'CERT']


def dashboard_title():
    st.markdown("""<h1 style='text-align: center'>
                Exploring the UK Data Engineer Job Market</h1>
                <hr style='height:2px;border-width:0;
                color:gray;background-color:gray'>""",
                unsafe_allow_html=True)


def centre_text(size, text, color='white', weight='normal'):
    return f"""<div style='text-align: center; color: {color}; 
    font-weight: {weight}; font-size: {size}px;'>{text}</div>"""


def tab_description():
    """Set the title and favicon of the tab"""
    st.set_page_config(page_title="Job-Scraper",
                       page_icon='random', layout="wide")


def dashboard_kpi():
    st.metric(label="Job Listings Count", value="")


def create_sidebar():
    """Create side bar for user selection."""
    st.sidebar.text("Filter Results")


def record_interactions():
    """Call function when a checkbox interaction has been made"""
    if st.session_state.checkbox:
        print("example checkbox has been selected")
    elif st.session_state.multiselect:
        pass


def create_checkbox_example():
    st.checkbox(label="Checkbox Name", value=False,
                on_change=record_interactions, key="checkbox")


def create_multiselect_example():
    choice = st.multiselect(label="Multiple Selection", options=(
        "1", "2", "3"), on_change=record_interactions, key="multiselect")
    return choice


def create_slider():
    """Create a slider option for varied ranges"""
    slider = st.slider("Slider Example", min_value=1, max_value=100, value=10)
    return slider


def get_date_input(today=date.today()):
    """Create a slider option for varied ranges"""
    date = st.date_input(
        label="Get Date", min_value=datetime.strptime('2023-11-01', "%Y-%M-%d"), max_value=today)
    return date


def setup():
    """Placeholder for constant attributes"""
    dashboard_title()
    create_sidebar()


def record_type_change():
    type_choices = st.session_state['type_choices']
    return type_choices


def display_requirement_count():
    """Multiselect option to display requirement count by requirement type."""
    choices = st.sidebar.multiselect(label="Select Requirement Type", options=(
        "HARD", "SOFT", "CERT", "PERK"), on_change=record_type_change, key='type_choices')
    return choices if choices else CHOICES


def set_type_df(response):
    df = pd.DataFrame(columns=response['columns'], data=response['rows'])
    return df[['Requirement', 'Requirement Type', 'Listing Count', 'Total Listings']]


if __name__ == "__main__":
    setup()
    type_df = set_type_df(select_top_requirements(10))
    type_choices = display_requirement_count()
    total_listings = type_df['Total Listings'].iloc[0]
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.markdown(centre_text(20, "Total Listings"), unsafe_allow_html=True)
        st.markdown(
            centre_text(20, total_listings, weight='bold'), unsafe_allow_html=True)
    st.markdown("---")
    st.dataframe(
        type_df.query("`Requirement Type` in @type_choices").drop('Total Listings', axis=1).head(10+1).reset_index(drop=True).shift()[1:])

    # create_checkbox_example()
    # create_multiselect_example()
    # create_slider()
    # get_date_input()
    hide_st_logos = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_logos, unsafe_allow_html=True)
