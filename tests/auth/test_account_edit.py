from tests.base_test import BaseTest

class TestAccountEdit(BaseTest):

    def test_account_edit_default_values(self):
        # Login first
        self.login_page.navigate()
        self.login_page.login("jose.lopez@gmail.com", "P@ssw0rd")

        # Go to edit account page
        self.account_edit_page.goto()
        assert self.account_edit_page.is_loaded(), "Edit Account page should be loaded"

        # Check default values (adjust expected values as needed)
        assert self.account_edit_page.firstname_input.input_value() == "Jose", "Default firstname should be Jose"
        assert self.account_edit_page.lastname_input.input_value() == "Lopez", "Default lastname should be Lopez"
        assert self.account_edit_page.email_input.input_value() == "jose.lopez@gmail.com", "Default email should match login"
        assert self.account_edit_page.telephone_input.input_value() == "77478459", "Default telephone should be empty or as expected"
        