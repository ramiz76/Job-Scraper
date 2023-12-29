import streamlit as st
import pandas as pd
import plotly.express as px


from utils import *
from queries import *


@st.cache_data
def get_listing_data():
    listing_data = select_listing_data()
    df_listing = pd.DataFrame(columns=listing_data.get(
        "columns"), data=listing_data.get("rows"))
    # df_listing.to_csv('dashboard/listings.csv', index=False)

    df_listing.dropna(subset=["requirement"], inplace=True)
    return df_listing


def roles_sidebar():
    title_categories = st.sidebar.multiselect(
        "Filter Titles", df_listing["title_category"].unique())
    if title_categories:
        df_filtered = df_listing[df_listing["title_category"].isin(
            title_categories)]
    else:
        df_filtered = df_listing.copy()
    title_levels = st.sidebar.multiselect(
        "Filter Experience Level", df_listing["title_level"].unique())
    if title_levels:
        df_filtered = df_filtered[df_filtered["title_level"].isin(
            title_levels)]
    locations = st.sidebar.multiselect(
        "Filter Locations", df_filtered["location"].unique())
    if locations:
        df_filtered = df_filtered[df_filtered["location"].isin(
            locations)]
    else:
        locations = df_listing["location"]
    salary_type = st.sidebar.multiselect(
        "Filter Salary Type", df_filtered["salary_type"].unique())
    if salary_type:
        df_filtered = df_filtered[df_filtered["salary_type"].isin(
            salary_type) & df_filtered["location"].isin(locations)]
    df_unique = df_filtered.drop_duplicates(subset="job_listing").copy()
    df_unique["avg_salary"] = (
        df_unique['low_salary'] + df_unique['high_salary']) / 2
    return df_unique


def create_title_salary_chart(df):
    df_grouped = df.groupby(by=["title_category"], as_index=False)[
        "avg_salary"].mean()
    chart = px.bar(df_grouped, x="title_category",
                   y="avg_salary", template="seaborn")
    st.plotly_chart(chart, use_container_width=True, height=200)


if __name__ == "__main__":
    df_listing = get_listing_data()
    # df_listing = df_listing.apply(group_titles, axis=1)
    df = roles_sidebar()
    create_title_salary_chart(df)
