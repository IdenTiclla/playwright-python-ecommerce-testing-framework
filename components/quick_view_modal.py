from playwright.sync_api import Page

class QuickViewModal():
    def __init__(self, page: Page):
        self.page = page
        self.container = "div#quick-view  div.modal-content"
        self.title = f"{self.container} h1"
        self.brand = f"{self.container} li:nth-of-type(1) a"
        self.product_code = f"{self.container} li:nth-of-type(2)  span:nth-of-type(2)"
        self.availability = f"{self.container} li:nth-of-type(3) span:nth-of-type(2)"
        self.price = f"{self.container} h3"
        self.close_button = f"{self.container} button[class*='close']"
        self.wishlist_button = f"{self.container} button[class*='btn-wishlist']"
        self.decrease_quantity_button = f"{self.container} button[data-spinner='down']"
        self.increase_quantity_button = f"{self.container} button[data-spinner='up']"
        self.add_to_cart_button = f"{self.container} button[class*='btn-cart']"
        self.buy_now_button = f"{self.container} button[class*='btn-buynow']"
        self.compare_button = f"{self.container} button[class*='btn-compare']"
        self.quantity = f"{self.container} input[name='quantity']"
        

    def get_title(self):
        return self.page.locator(self.title).text_content()
    
    def get_brand(self):
        return self.page.locator(self.brand).text_content()

    def is_available(self):
        return self.page.locator(self.availability).text_content() == "In Stock"

    def is_unavailable(self):
        return self.page.locator(self.availability).text_content() == "Out of Stock"

    def get_price(self):
        return self.page.locator(self.price).text_content()
    
    def get_quantity(self):
        return self.page.locator(self.quantity).text_content()
    
    def get_product_code(self):
        return self.page.locator(self.product_code).text_content()
    
    def add_to_wishlist(self):
        self.page.locator(self.wishlist_button).click()

    def add_to_cart(self):
        self.page.locator(self.add_to_cart_button).click()

    def get_add_to_cart_button_text(self):
        return self.page.locator(self.add_to_cart_button).text_content()
    
    def get_buy_now_button_text(self):
        return self.page.locator(self.buy_now_button).text_content()
    
    
    def close(self):
        self.page.locator(self.close_button).click()
    
