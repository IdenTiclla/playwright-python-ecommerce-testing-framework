from playwright.sync_api import Page

class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        
        # URLs
        self.register_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
        
        # Locators
        self.firstname_input = "input[name='firstname']"
        self.lastname_input = "input[name='lastname']"
        self.email_input = "input[name='email']"
        self.telephone_input = "input[name='telephone']"
        self.password_input = "input[name='password']"
        self.password_confirm_input = "input[name='confirm']"
        self.newsletter_yes_radio = "input[name='newsletter'][value='1']"
        self.newsletter_no_radio = "input[name='newsletter'][value='0']"
        self.privacy_policy_checkbox = "input[name='agree']"
        self.continue_button = "input[value='Continue']"
        self.login_link = "a:has-text('login page')"
        
    def navigate(self):
        """Navigate to register page"""
        self.page.goto(self.register_url)
        
    def register(self, firstname: str, lastname: str, email: str, telephone: str, 
                password: str, subscribe_newsletter: bool = False):
        """Fill in registration form and submit"""
        self.page.fill(self.firstname_input, firstname)
        self.page.fill(self.lastname_input, lastname)
        self.page.fill(self.email_input, email)
        self.page.fill(self.telephone_input, telephone)
        self.page.fill(self.password_input, password)
        self.page.fill(self.password_confirm_input, password)
        
        # Handle newsletter subscription with explicit wait and force-click
        if subscribe_newsletter:
            self.page.wait_for_selector(self.newsletter_yes_radio)
            self.page.click(self.newsletter_yes_radio, force=True)
        else:
            self.page.wait_for_selector(self.newsletter_no_radio)
            self.page.click(self.newsletter_no_radio, force=True)
            
        # Accept privacy policy
        self.page.wait_for_selector(self.privacy_policy_checkbox)
        self.page.click(self.privacy_policy_checkbox, force=True)
        
        # Submit form
        self.page.click(self.continue_button)
        
    def go_to_login(self):
        """Click on login page link"""
        self.page.click(self.login_link)