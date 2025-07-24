import os
from playwright.sync_api import expect
from tests.base_test import BaseTest
from utils.data_generator import generate_random_email, generate_random_password
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
            email=generate_random_email(),
            password=generate_random_password()
        )
        
        # Verify error message is displayeds
        assert self.login_page.alert_component.is_visible() == True
        expected_error_message = "Warning: No match for E-Mail Address and/or Password."
        actual_error_messages = self.login_page.alert_component.get_alert_messages()
        assert any(expected_error_message in alert_message for alert_message in actual_error_messages)



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

    def test_login_attempts_limit(self):
        # Navigate to login page
        self.login_page.navigate()


        # Try to login with invalid credentials
        email = generate_random_email()
        password = generate_random_password()

        for _ in range(5):
            self.login_page.login(
                email=email,
                password=password
            )

            # Verify error message is displayed
            assert self.login_page.alert_component.is_visible() == True
            expected_error_message = "Warning: No match for E-Mail Address and/or Password."
            actual_error_messages = self.login_page.alert_component.get_alert_messages()
            assert any(expected_error_message in alert_message for alert_message in actual_error_messages)

        self.login_page.login(
                email=email,
                password=password
            )

        # Verify error message is displayed
        assert self.login_page.alert_component.is_visible() == True
        expected_error_message = "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour."
        actual_error_messages = self.login_page.alert_component.get_alert_messages()
        assert any(expected_error_message in alert_message for alert_message in actual_error_messages)
