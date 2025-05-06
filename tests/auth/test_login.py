import os
import pytest
from pages.login_page import LoginPage
from playwright.sync_api import Page, expect

class TestLogin:
    @pytest.fixture
    def login_page(self, page: Page) -> LoginPage:
        return LoginPage(page)
    
    def test_user_can_login(self, login_page: LoginPage):
        # Navigate to login page
        login_page.navigate()
        
        # Login with valid credentials from environment variables
        email = os.getenv("VALID_EMAIL")
        password = os.getenv("VALID_PASSWORD")
        login_page.login(
            email=email,
            password=password
        )
        
        # Verify successful login (redirected to account page)
        expect(login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/account")

        assert login_page.page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/account"

    def test_invalid_login(self, login_page: LoginPage):
        # Navigate to login page
        login_page.navigate()
        
        # Try to login with invalid credentials
        login_page.login(
            email="invalid2@example.com",
            password="WrongPassword"
        )
        
        # Verify error message is displayed
        expect(login_page.page.locator(".alert-danger")).to_be_visible()
        expect(login_page.page.locator(".alert-danger")).to_contain_text("Warning: No match for E-Mail Address and/or Password")
        
    def test_forgotten_password(self, login_page: LoginPage):
        # Navigate to login page
        login_page.navigate()
        
        # Click forgotten password link
        login_page.click_forgotten_password()
        
        # Verify redirect to forgotten password page
        expect(login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/forgotten")
        
    def test_go_to_register(self, login_page: LoginPage):
        # Navigate to login page
        login_page.navigate()
        
        # Click register/continue link
        login_page.click_register()
        
        # Verify redirect to register page
        expect(login_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")



