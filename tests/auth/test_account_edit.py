import pytest
from pages.login_page import LoginPage
from pages.account_edit_page import AccountEditPage
from playwright.sync_api import expect, Page

class TestAccountEdit:
    @pytest.fixture
    def login_and_account_edit_pages(self, page: Page):
        login_page = LoginPage(page)
        account_edit_page = AccountEditPage(page)
        return login_page, account_edit_page
    
    def test_account_edit_default_values(self, login_and_account_edit_pages):
        login_page, account_edit_page = login_and_account_edit_pages
        
        # Login first
        login_page.navigate()
        login_page.login("jose.lopez@gmail.com", "P@ssw0rd")

        # Go to edit account page
        account_edit_page.goto()
        assert account_edit_page.is_loaded(), "Edit Account page should be loaded"

        # Check default values (adjust expected values as needed)
        assert account_edit_page.firstname_input.input_value() == "Jose", "Default firstname should be Jose"
        assert account_edit_page.lastname_input.input_value() == "Lopez", "Default lastname should be Lopez"
        assert account_edit_page.email_input.input_value() == "jose.lopez@gmail.com", "Default email should match login"
        assert account_edit_page.telephone_input.input_value() == "77478459", "Default telephone should be empty or as expected"
        