from playwright.sync_api import Page

class Alert:
    def __init__(self, page: Page):
        self.page = page
        self.alert = self.page.locator("div.container div.alert")

    def is_visible(self):
        return self.alert.is_visible()

    def get_alert_messages(self):
        return self.alert.all_text_contents()