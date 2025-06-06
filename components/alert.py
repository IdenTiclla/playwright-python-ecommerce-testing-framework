from playwright.sync_api import Page

class Alert:
    def __init__(self, page: Page):
        self.page = page
        self.alert = ".alert-success"

    def is_visible(self):
        return self.page.locator(self.alert).is_visible()

    def get_text(self):
        return self.page.locator(self.alert).text_content().strip()