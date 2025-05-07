from playwright.sync_api import Page

class CartPanel:
    def __init__(self, page: Page):
        self.page = page  # Fixed assignment
        self.panel = "div#cart-total-drawer"
        self.title = f"{self.panel} h5"
        self.message = f"{self.panel} p.text-center"
        self.sub_total = f"{self.panel} table:nth-child(2) tr:first-child td.text-right"
        self.total = f"{self.panel} table:nth-child(2) tr:last-child td.text-right"
        self.edit_button = f"{self.panel} div div.design-button:nth-child(1) > a"
        self.checkout_button = f"{self.panel} div div.design-button:nth-child(2) > a"

    def is_visible(self):
        return self.page.is_visible(self.panel)
    
    def check_message(self, expected_message: str):
        return self.page.inner_text(self.message) == expected_message

    def check_sub_total(self, expected_sub_total: str):
        return self.page.inner_text(self.sub_total) == expected_sub_total
    

    def check_total(self, expected_total: str):
        return self.page.inner_text(self.total) == expected_total