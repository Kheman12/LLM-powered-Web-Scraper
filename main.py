import streamlit as st
import time
import requests


# Function to validate the URL
def url_checker(url: str) -> bool:

    if not url.startswith(("http://", "https://")):
        return False

    
# Set page config
st.set_page_config(
    page_title="LLM POWERED AI SCRAPER",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar UI
with st.sidebar:
    st.header("Web Scraper Settings")
    url = st.text_input("Enter URL of the Website",placeholder="https://www.example.com")
    prompt = st.text_area("Describe the fields to be Extracted",placeholder="Scrape product's name,price,rating and reviews")
    st.markdown("----")
    scrape_button = st.button("Scrape")
    if scrape_button:
        if not url:
            st.error("Please enter the URL")
        elif not url_checker(url):
            st.error("URL is not Valid or Reachable")
        else:
            with st.spinner("Scraping data......",show_time=False):
                time.sleep(5)
                st.success("Sucessfully Scraped")

    
st.markdown("<h1 style='text-align: center;'>LLM POWERED WEB SCRAPER</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Developed By Kheman Saru</h3>",unsafe_allow_html=True)

