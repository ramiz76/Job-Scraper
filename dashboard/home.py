"""Homepage for Job-Scraper Dashboard"""
import streamlit as st
import pandas as pd

from static import homepage_title, tab_description, create_sidebar, hide_st_logos
from utils import centre_text, select_listing_count


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


if "__main__" == __name__:
    homepage_setup()
    homepage_kpi()
