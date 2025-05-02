from playwright.sync_api import Page

class AccountEditPage:
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/edit"

    def __init__(self, page: Page):
        self.page = page
        self.firstname_input = "#input-firstname"
        self.lastname_input = "#input-lastname"
        self.email_input = "#input-email"
        self.telephone_input = "#input-telephone"
        self.continue_button = "input[type='submit'][value='Continue']"
        self.success_alert = ".alert-success"
        self.breadcrumb = ".breadcrumb li.active"

    def goto(self):
        self.page.goto(self.URL)

    def is_loaded(self):
        return self.page.locator(self.breadcrumb).is_visible()

    def fill_firstname(self, firstname: str):
        self.page.fill(self.firstname_input, firstname)

    def fill_lastname(self, lastname: str):
        self.page.fill(self.lastname_input, lastname)

    def fill_email(self, email: str):
        self.page.fill(self.email_input, email)

    def fill_telephone(self, telephone: str):
        self.page.fill(self.telephone_input, telephone)

    def submit(self):
        self.page.click(self.continue_button)

    def is_success_alert_visible(self):
        return self.page.locator(self.success_alert).is_visible()
