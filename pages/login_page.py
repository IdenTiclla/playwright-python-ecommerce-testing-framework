from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
        # URLs
        self.login_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
        
        # Locators
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = "input[value='Login']"
        self.forgotten_password_link = "form a[href*='route=account/forgotten']"
        self.register_link = "p + a[href*='route=account/register']"
        
    def navigate(self):
        """Navigate to login page"""
        self.page.goto(self.login_url)
        
    def login(self, email: str, password: str):
        """Login with the given credentials"""
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
        
    def click_forgotten_password(self):
        """Click on forgotten password link"""
        self.page.click(self.forgotten_password_link)
        
    def click_register(self):
        """Click on register/continue link"""
        self.page.click(self.register_link)