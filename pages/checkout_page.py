from pages.base_page import BasePage
from playwright.sync_api import Page
from components.header_actions import HeaderActions
from components.billing_address_form import BillingAddressForm
class CheckoutPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Components
        self.header_actions = HeaderActions(page)
        self.billing_address_form = BillingAddressForm(page)
        
        # Locators
        self.login_radio = page.locator("#input-account-login")
        self.register_radio = page.locator("#input-account-register")
        self.guest_radio = page.locator("#input-account-guest")
        self.comment_input = self.page.locator("textarea#input-comment")
        self.terms_and_conditions_checkbox = self.page.locator("input[name='agree']")
        self.continue_button = self.page.locator("button#button-save")


    def is_login_radio_selected(self):
        """Check if the login radio is selected"""
        return self.login_radio.is_checked()

    def is_register_radio_selected(self):
        """Check if the register radio is selected"""
        return self.register_radio.is_checked()

    def is_guest_radio_selected(self):
        """Check if the guest radio is selected"""
        return self.guest_radio.is_checked()

    def account_radio_options_are_displayed(self):
        """Check if the account radio options are displayed"""
        return self.login_radio.is_visible() and self.register_radio.is_visible() and self.guest_radio.is_visible()

    def fill_comment_input(self, comment: str):
        """Fill the comment input"""
        self.comment_input.fill(comment)

    def accept_terms_and_conditions(self):
        """Fill the terms and conditions checkbox"""
        self.terms_and_conditions_checkbox.click(force=True)

    def click_continue_button(self):
        """Click the continue button"""
        self.continue_button.click()
