import time
from tests.base_test import BaseTest
from playwright.sync_api import expect
from utils.data_generator import generate_random_email, generate_random_first_name, generate_random_last_name, generate_random_phone_number, generate_random_password
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
            subscribe_newsletter=True,
            accept_terms=True
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

    def test_trying_to_register_without_accepting_terms_and_conditions(self):
        # Navigate to register page
        self.register_page.navigate()

        # Fill in registraation form with valid data

        first_name = generate_random_first_name()
        last_name = generate_random_last_name()
        email = generate_random_email()
        telephone = generate_random_phone_number()
        password = generate_random_password()
        password_confirm = password

        # Try to register without accepting terms and conditions
        self.register_page.register(
            firstname=first_name,
            lastname=last_name,
            email=email,
            telephone=telephone,
            password=password,
            password_confirm=password_confirm,
            subscribe_newsletter=False,
            accept_terms=False
        )
        # Verify that the error message is visible
        actual_alert_messages = self.register_page.alert_component.get_alert_messages()
        expected_error_message = "Warning: You must agree to the Privacy Policy!"
        assert any(expected_error_message in alert_message for alert_message in actual_alert_messages)


    def test_edit_account_default_values(self):
        # Navigate to register page
        self.register_page.navigate()

        # Fill in registraation form with valid data
        first_name = generate_random_first_name()
        last_name = generate_random_last_name()
        email = generate_random_email()
        telephone = generate_random_phone_number()
        password = generate_random_password()
        password_confirm = password

        # Fill in registraation form with valid data
        self.register_page.register(
            firstname=first_name,
            lastname=last_name,
            email=email,
            telephone=telephone,
            password=password,
            password_confirm=password_confirm,
            subscribe_newsletter=True,
            accept_terms=True
        )

        # go to edit account page
        self.account_edit_page.navigate()

        # assert that the url is correct
        expect(self.account_edit_page.page).to_have_url("https://ecommerce-playground.lambdatest.io/index.php?route=account/edit")
        
        # wait for page to be fully loaded
        self.account_edit_page.page.wait_for_load_state("networkidle")

        # verify that the default values are filled in
    
        first_name_value = self.account_edit_page.get_first_name_value()
        last_name_value = self.account_edit_page.get_last_name_value()
        email_value = self.account_edit_page.get_email_value()
        telephone_value = self.account_edit_page.get_telephone_value()

        assert first_name_value == first_name, f"Expected first name to be '{first_name}', but got '{first_name_value}'"
        assert last_name_value == last_name, f"Expected last name to be '{last_name}', but got '{last_name_value}'"
        assert email_value == email, f"Expected email to be '{email}', but got '{email_value}'"
        assert telephone_value == telephone, f"Expected telephone to be '{telephone}', but got '{telephone_value}'"
