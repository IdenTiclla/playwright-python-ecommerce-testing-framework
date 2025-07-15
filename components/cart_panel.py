from playwright.sync_api import Page

class CartPanel:
    def __init__(self, page: Page):
        self.page = page
        self.panel = page.locator("div#cart-total-drawer")
        self.title = self.page.locator("div#cart-total-drawer h5")
        self.message = self.page.locator("div#cart-total-drawer p.text-center")
        self.sub_total = self.page.locator("//td[text()='Sub-Total:']/following-sibling::td")
        self.total = self.page.locator("//td[text()='Total:']/following-sibling::td")
        self.edit_button = self.page.locator("div#cart-total-drawer a[href*='route=checkout/cart']")
        self.checkout_button = self.page.locator("div#cart-total-drawer a[href*='route=checkout/checkout']")
        self.x_button = self.page.locator("div#cart-total-drawer button.close")

    def is_visible(self):
        return self.panel.is_visible()
    
    def get_message(self):
        return self.message.inner_text()

    def get_sub_total(self):
        return self.sub_total.inner_text()
    
    def get_total(self):
        return self.total.inner_text()