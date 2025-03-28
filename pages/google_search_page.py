from playwright.sync_api import Page
import logging
from components.submit_button import SubmitButton

class GoogleSearchPage:
    def __init__(self, page: Page):
        self.page = page
        # Define CSS selectors as properties
        self.search_input_selector = 'textarea[name="q"]'
        self.submit_button = SubmitButton(page, 'input[type="submit"]')  # Use the SubmitButton component

    def search(self, query: str):
        logging.info(f"Searching for: {query}")
        self.page.fill(self.search_input_selector, query)
        self.submit_button.click()  # Reuse the submit button component

    def get_title(self) -> str:
        return self.page.title()
