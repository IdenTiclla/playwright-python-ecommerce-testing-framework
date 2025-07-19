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

    def get_page_title(self):
        return self.page_title.text_content().strip()
    
    def get_empty_cart_message(self):
        return self.empty_cart_message.text_content().strip()