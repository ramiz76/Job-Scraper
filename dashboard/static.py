"""This module contains functions that are used for static streamlit displays."""
import streamlit as st
from utils import centre_text


def hide_st_logos():
    hide_st_logos = """ <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style> """
    st.markdown(hide_st_logos, unsafe_allow_html=True)


def dashboard_title():
    """Display dashboard title."""
    st.markdown("""<h1 style='text-align: center'>
                Exploring the UK Data Engineer Job Market</h1>
                <hr style='height:2px;border-width:0;
                color:gray;background-color:gray'>""",
                unsafe_allow_html=True)


def tab_description():
    """Set the title and favicon of the tab"""
    st.set_page_config(page_title="Job-Scraper",
                       page_icon='random', layout="wide")


def create_sidebar():
    """Create side bar for user selection."""
    st.sidebar.text("Filter Results")


def home_set_left_column(type_df, type_choices):
    # type_df = type_df.drop('Total Listings', axis=1)
    type_df = type_df.reset_index(drop=True).shift()[1:]
    st.dataframe(
        type_df.query("`Requirement Type` in @type_choices"))
