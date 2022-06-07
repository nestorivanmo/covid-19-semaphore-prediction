import streamlit as st
import numpy as np
from pandas import DataFrame
import os
import validators
from url_utils import extract_content

st.set_page_config(
    page_title="COVID Semaphore Prediction",
    page_icon="🚦",
)

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

st.title("COVID-19 Semaphore Prediction")
st.header("")

st.markdown("## ℹ️ How to use this app?")
st.write(
    """
    - By pasting a URL to any mexican news site and find out the COVID-19's semaphore color for **0**, **2**, **4** and **8 weeks** since the news' publication date
    - 📰 -> 🚦
    """
)
st.markdown("")

st.markdown("## 📰 News Finder")
news_url = st.text_area(
    "Paste the URL of any mexican news site",
    height=50
)
semaphore_button = st.button("Find out semaphore's color")

if semaphore_button:
    if len(news_url) == 0:
        st.warning('Please make sure that you write any URL')
        st.stop()
    if not validators.url(news_url):
        st.warning('Please make sure that you write a valid URL')
        st.stop()
else:
    st.stop()

st.markdown("## 🚦 Semaphore prediction")
data = extract_content(news_url)
st.write(data)
