from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.config import BASE_URL

class SuccessPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # URLs
        self.success_url = f"{BASE_URL}/index.php?route=account/success"

        # Locators
        self.page_title = self.page.locator("div.content h1")
        self.continue_button = self.page.locator("div.content a.btn.btn-primary")

    def get_page_title(self):
        return self.page_title.text_content().strip()




