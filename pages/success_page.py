from pages.base_page import BasePage
from playwright.sync_api import Page

class SuccessPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # URLs
        self.success_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/success"

        # Locators
        self.page_title = self.page.locator("div.content h1")
        self.continue_button = self.page.locator("div.content a.btn.btn-primary")

    def get_page_title(self):
        return self.page_title.text_content().strip()




