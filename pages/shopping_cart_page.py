from pages.base_page import BasePage
from playwright.sync_api import Page

class ShoppingCartPage(BasePage):
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart"

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.page_title = self.page.locator("div.content h1")
        self.empty_cart_message = self.page.locator("div.content p")
        self.continue_button = self.page.locator("div.content a.btn.btn-primary")
        self.products = "div#content div.table-responsive tbody tr"

    def get_page_title(self):
        return self.page_title.text_content().strip()
    
    def get_empty_cart_message(self):
        return self.empty_cart_message.text_content().strip()
    
    def get_quantity_of_products(self):
        return self.page.locator(self.products).count()
    
    def shopping_cart_contains_product(self, product_name):
        product_names = self.page.locator(self.products).locator("td:nth-of-type(2)").all_text_contents()
        return any(product_name in name for name in product_names)
    
    def get_product_name(self, index):
        product_name = self.page.locator(self.products).locator("td:nth-of-type(2)").nth(index).text_content().strip()
        return product_name

    def get_product_quantity(self, index):
        product_quantity = self.page.locator(self.products).locator("input").nth(index).input_value()
        return int(product_quantity)
    
    def get_unit_price(self, index):
        unit_price = self.page.locator(self.products).locator("td:nth-of-type(5)").nth(index).text_content().strip("$")
        return round(float(unit_price), 2)
    
    def get_total_price(self, index):
        total_price = self.page.locator(self.products).locator("td:nth-of-type(6)").nth(index).text_content().strip("$")
        return round(float(total_price), 2)