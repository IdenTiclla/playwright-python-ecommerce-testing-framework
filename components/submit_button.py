from playwright.sync_api import Page

class SubmitButton:
    def __init__(self, page: Page, selector: str):
        self.page = page
        self.selector = selector

    def click(self):
        self.page.click(self.selector)
