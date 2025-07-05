from playwright.sync_api import Page

class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        
        # URLs
        self.register_url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
        
        # Locators
        self.firstname_input = page.locator("input[name='firstname']")
        self.lastname_input = page.locator("input[name='lastname']")
        self.email_input = page.locator("input[name='email']")
        self.telephone_input = page.locator("input[name='telephone']")
        self.password_input = page.locator("input[name='password']")
        self.password_confirm_input = page.locator("input[name='confirm']")
        self.password_error = page.locator("//input[@id='input-confirm']/following-sibling::div[@class='text-danger']")
        self.newsletter_yes_radio = page.locator("input[name='newsletter'][value='1']")
        self.newsletter_no_radio = page.locator("input[name='newsletter'][value='0']")
        self.privacy_policy_checkbox = page.locator("input[name='agree']")
        self.continue_button = page.locator("input[value='Continue']")
        self.login_link = page.locator("a:has-text('login page')")


    def navigate(self):
        """Navigate to register page"""
        self.page.goto(self.register_url)
        
    def register(self, firstname: str, lastname: str, email: str, telephone: str, 
                password: str, password_confirm: str, subscribe_newsletter: bool = False):
        """Fill in registration form and submit"""
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.email_input.fill(email)
        self.telephone_input.fill(telephone)
        self.password_input.fill(password)
        self.password_confirm_input.fill(password_confirm)


        # Handle newsletter subscription with explicit wait and force-click
        if subscribe_newsletter:
            self.newsletter_yes_radio.wait_for()
            self.newsletter_yes_radio.click(force=True)
        else:
            self.newsletter_no_radio.wait_for()
            self.newsletter_no_radio.click(force=True)
            
        # Accept privacy policy
        self.privacy_policy_checkbox.wait_for()
        self.privacy_policy_checkbox.click(force=True)

        # Submit form
        self.continue_button.click()
        
    def go_to_login(self):
        """Click on login page link"""
        self.login_link.click()

    def password_error_visible(self):
        """Check if password error message is visible"""
        return self.password_error.is_visible()
    
    def get_password_error_text(self):
        """Get the text of the password error message"""
        return self.password_error.inner_text() if self.password_error.is_visible() else None