from pages.base_page import BasePage
from playwright.sync_api import Page
from components.header_actions import HeaderActions

class CheckoutPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Components
        self.header_actions = HeaderActions(page)

        # Locators
        self.login_radio = page.locator("#input-account-login")
        self.register_radio = page.locator("#input-account-register")
        self.guest_radio = page.locator("#input-account-guest")


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
