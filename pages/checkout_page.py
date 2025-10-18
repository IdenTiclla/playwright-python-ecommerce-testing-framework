from pages.base_page import BasePage
from playwright.sync_api import Page
from components.header_actions import HeaderActions

class CheckoutPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Components
        self.header_actions = HeaderActions(page)
