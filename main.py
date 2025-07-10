import asyncio
import sys
import streamlit as st
import time
import requests
from streamlit_tags import st_tags_sidebar
from parse import LLMParser
from processing import extract_body_content, clean_body_content, convert_to_markdown
from scrape import extract_html
import pandas as pd
import json
import random

parser = LLMParser()

# Function when the Scrape Button is clicked:
async def scrape_action(url, fields):
    raw_html = await extract_html(url)
    body_content = extract_body_content(raw_html)
    clean_html = clean_body_content(body_content)
    markdown = convert_to_markdown(clean_html)
    output = parser.parse(markdown, fields)
    return output

def json_to_df(json_data: dict) -> pd.DataFrame:
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                return pd.DataFrame(value)
    return pd.DataFrame()

# Set page config
st.set_page_config(
    page_title="LLM POWERED AI SCRAPER",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar UI
with st.sidebar:
    st.header("Web Scraper Settings")
    url = st.text_input("Enter URL of the Website", placeholder="https://www.example.com")
    tags = st_tags_sidebar(
        label='Enter Fields to Extract:',
        text='Press enter to add a tag',
        value=[],
        suggestions=[],
        maxtags=-1,
        key='tags_input'
    )
    fields = tags   
    st.markdown("----")

    if 'scrape_button' not in st.session_state:
        st.session_state['scrape_button'] = False
    
    if st.button("Scrape"):
        if not tags:
            st.error("Please enter the Tags!")
        elif not url:
            st.error("Please enter the URL")
        else:
            with st.spinner("Scraping data......"):
                try:
                    # Create a new event loop for Windows
                    if sys.platform.startswith("win"):
                        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                    
                    output = asyncio.run(scrape_action(url, fields))
                    st.session_state['results'] = output
                    st.session_state['scrape_button'] = True
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

st.markdown("<h1 style='text-align: center;'>LLM POWERED WEB SCRAPER</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Developed By Kheman Saru</h3>", unsafe_allow_html=True)
st.markdown("---")

if st.session_state.get('scrape_button'):
    scraped_data = st.session_state['results']
    df = json_to_df(scraped_data)
    st.write("Here are the Scraped data:", df)

    col1, col2 = st.columns(2)
    random_num = random.randint(1, 100)
    with col1:
        st.download_button(
            label="Download JSON",
            data=json.dumps(scraped_data, indent=4),
            file_name=f"scraped_data_json{random_num}.json",
            mime="application/json"
        )
    with col2:
        st.download_button(
            label="Download Excel",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"scraped_data_excel{random_num}.csv",
            mime="text/csv"
        )