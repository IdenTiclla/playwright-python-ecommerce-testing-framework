import pytest
import time
from tests.base_test import BaseTest
from pages.register_page import RegisterPage
from playwright.sync_api import Page, expect

class TestRegister(BaseTest):
    
    def test_user_can_register(self):
        # Navigate to register page
        self.register_page.navigate()
        
        # Register new user with unique email
        self.register_page.register(
            firstname="Test",
            lastname="User",
            email="test.user" + str(int(time.time())) + "@example.com",
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@123",  # Same password for confirmation
            subscribe_newsletter=True
        )
        
        # Verify registration success (you can add appropriate assertions here)
        # For example, check if redirected to success page or account page

        expect(self.register_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/success")
        # check that the url contain
        assert "success" in self.register_page.page.url
        expect(self.register_page.page.locator("h1")).to_have_text("Your Account Has Been Created!")
        
    def test_validation_errors(self):
        # Navigate to register page
        self.register_page.navigate()
        
        # Try to register without filling required fields
        self.register_page.page.click("input[value='Continue']")
        
        # Verify error messages are displayed
        expect(self.register_page.page.locator("input#input-firstname + div.text-danger")).to_be_visible()
        expect(self.register_page.page.locator("input#input-lastname + div.text-danger")).to_be_visible()
        expect(self.register_page.page.locator("input#input-email + div.text-danger")).to_be_visible()
        expect(self.register_page.page.locator("input#input-telephone + div.text-danger")).to_be_visible()
        expect(self.register_page.page.locator("input#input-password + div.text-danger")).to_be_visible()
        expect(self.register_page.page.locator(".alert-danger")).to_be_visible()
        
    def test_go_to_login_page(self):
        # Navigate to register page
        self.register_page.navigate()
        
        # Click on login page link
        self.register_page.go_to_login()
        
        # Verify redirect to login page
        expect(self.register_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

    def test_password_confirmation_mismatch(self):
        # Navigate to register page
        self.register_page.navigate()
        
        # Fill in registration form with mismatched passwords
        self.register_page.register(
            firstname="Test",
            lastname="User",
            email="test.user" + str(int(time.time())) + "@example.com",
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@456",  # Mismatched password
            subscribe_newsletter=True
        )

        # Verify that the error message is visible
        assert self.register_page.password_error_visible(), "Password confirmation error message should be visible"
        # Verify the text of the error message
        password_error_text = self.register_page.get_password_error_text()
        assert password_error_text == "Password confirmation does not match password!", f"Expected error message to be 'Password confirmation does not match password!', but got '{password_error_text}'"