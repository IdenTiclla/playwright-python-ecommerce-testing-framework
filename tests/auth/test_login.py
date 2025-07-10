import os
from playwright.sync_api import expect
from tests.base_test import BaseTest

class TestLogin(BaseTest):
    
    def test_user_can_login(self):
        # Navigate to login page
        self.login_page.navigate()
        
        # Login with valid credentials from environment variables
        email = os.getenv("VALID_EMAIL")
        password = os.getenv("VALID_PASSWORD")
        self.login_page.login(
            email=email,
            password=password
        )
        
        # Verify successful login (redirected to account page)
        expect(self.login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/account")

        assert self.login_page.page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/account"

    def test_invalid_login(self):
        # Navigate to login page
        self.login_page.navigate()
        
        # Try to login with invalid credentials
        self.login_page.login(
            email="invalid33@example.com",
            password="WrongPassword"
        )
        
        # Verify error message is displayeds
        assert self.login_page.alert_component.is_visible() == True
        expected_error_message = "Warning: No match for E-Mail Address and/or Password."
        actual_error_message = self.login_page.alert_component.get_text()
        assert actual_error_message == expected_error_message



    def test_forgotten_password(self):
        # Navigate to login page
        self.login_page.navigate()
        
        # Click forgotten password link
        self.login_page.click_forgotten_password()
        
        # Verify redirect to forgotten password page
        expect(self.login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/forgotten")
        
    def test_go_to_register(self):
        # Navigate to login page
        self.login_page.navigate()

        # Click register/continue link
        self.login_page.click_register()
        
        # Verify redirect to register page
        expect(self.login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")



