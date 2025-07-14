from playwright.sync_api import Page

class AccountEditPage:
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/edit"

    def __init__(self, page: Page):
        self.page = page
        self.firstname_input = page.locator("#input-firstname")
        self.lastname_input = page.locator("#input-lastname")
        self.email_input = page.locator("#input-email")
        self.telephone_input = page.locator("#input-telephone")
        self.continue_button = page.locator("input[type='submit'][value='Continue']")
        self.success_alert = page.locator(".alert-success")
        self.breadcrumb = page.locator(".breadcrumb li.active")

    def goto(self):
        self.page.goto(self.URL)

    def is_loaded(self):
        return self.breadcrumb.is_visible()

    def fill_firstname(self, firstname: str):
        self.firstname_input.fill(firstname)

    def fill_lastname(self, lastname: str):
        self.lastname_input.fill(lastname)

    def fill_email(self, email: str):
        self.email_input.fill(email)

    def fill_telephone(self, telephone: str):
        self.telephone_input.fill(telephone)

    def submit(self):
        self.continue_button.click()

    def is_success_alert_visible(self):
        return self.success_alert.is_visible()
    

    def get_first_name_value(self):
        return self.firstname_input.input_value()

    def get_last_name_value(self):
        return self.lastname_input.input_value()

    def get_email_value(self):
        return self.email_input.input_value()
    
    def get_telephone_value(self):
        return self.telephone_input.input_value()
