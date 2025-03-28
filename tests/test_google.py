import os
import logging
from playwright.sync_api import sync_playwright
from pages.google_search_page import GoogleSearchPage

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    search_query = os.getenv('SEARCH_QUERY', 'python')  # Use environment variable for query
    google_url = 'https://www.google.com'  # URL can also be moved to a config file

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(google_url)

        google_search = GoogleSearchPage(page)
        google_search.search(search_query)

        page.wait_for_timeout(5000)

        browser.close()

if __name__ == '__main__':
    main()
