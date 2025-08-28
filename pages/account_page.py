from playwright.sync_api import Page
from components.sidebar_navigation import SidebarNavigation
from utils.config import BASE_URL

class AccountPage:
    
    @property
    def url(self):
        return f"{BASE_URL}/index.php?route=account/account"

    def __init__(self, page: Page):
        self.page = page
        # Components
        self.sidebar_navigation = SidebarNavigation(page)
        

    def goto(self):
        self.page.goto(self.url)

    def wait_for_page_load(self):
        """Wait for the account page to fully load"""
        self.page.wait_for_load_state("domcontentloaded")