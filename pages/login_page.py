from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # URLs
        self.login_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
        
        # Locators
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("input[value='Login']")
        self.forgotten_password_link = page.locator("form a[href*='route=account/forgotten']")
        self.register_link = page.locator("p + a[href*='route=account/register']")
        
    def navigate(self):
        """Navigate to login page"""
        self.page.goto(self.login_url)
        
    def login(self, email: str, password: str):
        """Login with the given credentials"""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        
    def click_forgotten_password(self):
        """Click on forgotten password link"""
        self.forgotten_password_link.click()
        
    def click_register(self):
        """Click on register/continue link"""
        self.register_link.click()

    def wait_for_page_load(self):
        """Wait for the login page to fully load"""
        self.page.wait_for_load_state("domcontentloaded")