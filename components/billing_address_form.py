from playwright.sync_api import Page
from components.base_component import BaseComponent

class BillingAddressForm(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.firstname_input = page.locator("input[name='firstname']")
        self.lastname_input = page.locator("input[name='lastname']")
        self.company_input = page.locator("input[name='company']")
        self.address_1_input = page.locator("input[name='address_1']")
        self.address_2_input = page.locator("input[name='address_2']")
        self.city_input = page.locator("input[name='city']")
        self.postcode_input = page.locator("input[name='postcode']")
        self.country_select = page.locator("select[name='country_id']")
        self.zone_select = page.locator("select[name='zone_id']")


    def fill_billing_address_form(self, firstname: str, lastname: str, company: str, address_1: str, address_2: str, city: str, postcode: str, country: str, zone: str):
        """Fill the billing address form"""
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.company_input.fill(company)
        self.address_1_input.fill(address_1)
        self.address_2_input.fill(address_2)
        self.city_input.fill(city)
        self.postcode_input.fill(postcode)
        self.country_select.select_option(country)
        self.zone_select.select_option(zone)