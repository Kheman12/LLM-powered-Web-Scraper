from patchright.sync_api import sync_playwright
import random 
import time 


def load_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\A C E R\OneDrive\Desktop\LLM powered AI Scraper\user_data",
            channel="chrome",
            headless=False,
            no_viewport=True
        )
        page = browser.new_page()
        page.goto(url)
        time.sleep(random.randint(2,6))
        raw_html = page.content()
        browser.close()
        return raw_html
        