"""This module contains functions that are used for static streamlit displays."""
import streamlit as st
import pandas as pd


def tab_description():
    """Set the title and favicon of the tab"""
    st.set_page_config(page_title="Job-Scraper",
                       page_icon='random', layout="wide")


def hide_st_logos():
    """Hide streamlit logos"""
    hide_st_logos = """ <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style> """
    st.markdown(hide_st_logos, unsafe_allow_html=True)


def create_sidebar():
    """Create side bar for user selection."""
    st.sidebar.header("Filter Results")


def homepage_title():
    """Display dashboard title."""
    st.markdown("""<h1 style='text-align: center'>
                Exploring the UK Data Engineer Job Market</h1>
                <hr style='height:2px;border-width:0;
                color:gray;background-color:gray'>""",
                unsafe_allow_html=True)


def home_set_left_column(type_df, type_choices, column):
    # type_df = type_df.drop('Total Listings', axis=1)
    type_df = type_df.reset_index(drop=True).shift()[1:]
    st.dataframe(
        type_df.query(f"`{column}` in @type_choices"))
