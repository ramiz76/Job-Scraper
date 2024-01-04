"""Homepage for Job-Scraper Dashboard"""
import streamlit as st
import pandas as pd

from static import *
from utils import *


def homepage_setup():
    """Placeholder for static dashboard displays."""
    tab_description()
    homepage_title()
    create_sidebar()
    # hide_st_logos()


def homepage_kpi():
    l_kpi, m_kpi, r_kpi = st.columns([3, 1, 1])
    listing_count = select_listing_count()
    with l_kpi:
        st.markdown(centre_text(20, "Total Listings"), unsafe_allow_html=True)
        st.markdown(
            centre_text(20, listing_count.get('rows')[0][0], weight='bold'), unsafe_allow_html=True)
    st.markdown("---")


def filter_roles():
    df_filtered = df_listing.copy()
    # exploded_skills = df_filtered['requirements_list'].explode()
    # exploded_skills = exploded_skills.str.split(', ').explode()
    # skills_count = exploded_skills.value_counts()
    # sorted_skills = skills_count.index.tolist()
    selected_skills = st.multiselect(
        "Please Select Your Skills", sorted_skills)
    df_filtered = df_filtered[df_filtered['requirements_list'].apply(
        lambda x: any(skill in x for skill in selected_skills))]
    df_filtered['skills_match_percentage'] = df_filtered['requirements_list'].apply(
        lambda x: calculate_skills_match(x, selected_skills))
    df_filtered['num_matched_skills'] = df_filtered['requirements_list'].apply(
        lambda x: count_matched_skills(x, selected_skills))
    title_categories = st.sidebar.multiselect(
        "Job Title", df_listing["title_category"].unique())
    if title_categories:
        df_filtered = df_filtered[df_filtered["title_category"].isin(
            title_categories)]
    title_levels = st.sidebar.multiselect(
        "Experience Level", df_filtered["title_level"].unique())
    if title_levels:
        df_filtered = df_filtered[df_filtered["title_level"].isin(
            title_levels)]
    locations = st.sidebar.multiselect(
        "Location", df_filtered["location"].unique())
    if locations and locations != [None]:
        df_filtered = df_filtered[df_filtered["location"].isin(
            locations)]
    salary_type = st.sidebar.multiselect(
        "Salary Type", df_filtered["salary_type"].unique())
    if salary_type:
        df_filtered = df_filtered[df_filtered["salary_type"].isin(
            salary_type)]
    df_unique = df_filtered.drop_duplicates(subset="job_listing").copy()
    df_unique = df_filtered.sort_values(
        by=['skills_match_percentage', 'num_matched_skills'], ascending=[False, False])
    # return df_unique
    show_listings(df_unique, selected_skills)


def count_matched_skills(listing_skills, selected_skills):
    """Count the number of selected skills that match the listing skills."""
    if not listing_skills or not selected_skills:
        return 0
    listing_skills_set = set(listing_skills.replace(" ", "").split(","))
    selected_skills_set = set(selected_skills)
    return len(listing_skills_set.intersection(selected_skills_set))


def show_listings(df, selected_skills=[]):
    """find the number of matching skills to listing and order by percentage of match to listing
    match by how much your skills match with listing AND
    match by how many of your skills fit within the requirements (red/yellow/green to show how strong fit it is )
    another dataframe could show suggested roles based on matches   
    """
    for index, row in df.iterrows():
        # skills_match_percentage = calculate_skills_match(
        #     row['requirements_list'], selected_skills)
        st.markdown(f"**Skills Match**: {row['skills_match_percentage']}%")
        st.markdown(
            f"### [{row['title']}]({row['url']})", unsafe_allow_html=True)
        st.markdown(
            f"**Company**: [{row['company']}]({row.get('company_url')})",
            unsafe_allow_html=True)
        if row["salary_type"] == "competitive" or row["salary_type"] == "unspecified":
            salary = 'Competitive'
        else:
            if row["low_salary"] == row["high_salary"]:
                salary = f'£{format(row["high_salary"], ",")}'
            else:
                salary = f'£{format(row["low_salary"],",")} - £{format(row["high_salary"], ",")}'

        st.markdown(f"**Salary**: {salary}")

        st.markdown(f"**Skills Required**: {row['requirements_list']}")
        st.markdown(
            f"<div style='text-align: right;'><strong>Date Posted:</strong> {row.get('posting_date')}</div>", unsafe_allow_html=True)

        st.write("---")


def calculate_skills_match(listing_skills, selected_skills):
    """Calculate the percentage of selected skills that match the listing skills."""
    if not listing_skills or not selected_skills:
        return 0

    listing_skills_set = set(listing_skills.replace(" ", "").split(","))
    selected_skills_set = set(selected_skills)
    matching_skills = listing_skills_set.intersection(selected_skills_set)
    if not matching_skills:
        return 0
    match_percentage = len(matching_skills) / len(listing_skills_set) * 100
    return round(match_percentage, 2)


if "__main__" == __name__:
    homepage_setup()
    homepage_kpi()
    skills = select_query(QUERY_skill_ordered)
    skills_df = pd.DataFrame(skills['rows'], columns=skills['columns'])
    sorted_skills = skills_df['requirement'].tolist()
    df_listing = static_get_listing_data()
    filter_roles()
    # show_listings(filter_roles())
    # Add option to filter listings by MUST HAVE skills - if high match but not AWS as skill then exclude
    # Add option to order by 'match by your requirements' and 'match by listings requirements'
    # If selected skill matches, then highlight it green (maybe add this?)
    # add two sliders for salary and date posted
