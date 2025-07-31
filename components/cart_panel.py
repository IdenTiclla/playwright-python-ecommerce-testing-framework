from playwright.sync_api import Page

class CartPanel:
    def __init__(self, page: Page):
        self.page = page
        self.panel = page.locator("div#cart-total-drawer")
        self.title = self.page.locator("div#cart-total-drawer h5")
        self.message = self.page.locator("div#cart-total-drawer p.text-center")
        self.sub_total = self.page.locator("//td[text()='Sub-Total:']/following-sibling::td")
        self.total = self.page.locator("//td[text()='Total:']/following-sibling::td")
        self.edit_cart_button = self.page.locator("div#cart-total-drawer a[href*='route=checkout/cart']")
        self.checkout_button = self.page.locator("div#cart-total-drawer a[href*='route=checkout/checkout']")
        self.x_button = self.page.locator("div#cart-total-drawer h5 a")

    def is_visible(self):
        return self.panel.is_visible()
    
    def get_message(self):
        return self.message.inner_text()

    def get_sub_total(self):
        return round(float(self.sub_total.inner_text().strip("$")), 2)
    
    def get_total(self):
        return round(float(self.total.inner_text().strip("$")), 2)
    
    def click_on_edit_cart_button(self):
        self.edit_cart_button.click()

    def close_cart_panel(self):
        self.x_button.click()

    def get_product_names(self):
        return self.panel.locator("table:first-child td:nth-child(2) a").all_inner_texts()
    
    def get_product_total_quantities(self):
        quantities = self.panel.locator("table:first-child tr td:nth-of-type(3)").all_inner_texts()
        quantities = [int(quantity.replace("x", "")) for quantity in quantities]
        return sum(quantities)