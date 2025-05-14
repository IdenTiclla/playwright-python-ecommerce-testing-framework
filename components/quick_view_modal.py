from playwright.sync_api import Page

class QuickViewModal():
    def __init__(self, page: Page):
        self.page = page
        self.modal = page.locator("div#quick-view  div.modal-content")
        self.title = self.modal.locator("h1")
        self.brand = self.modal.locator("li:nth-of-type(1) a")
        self.product_code = self.modal.locator("li:nth-of-type(2)  span:nth-of-type(2)")
        self.availability = self.modal.locator("li:nth-of-type(3) span:nth-of-type(2)")
        self.price = self.modal.locator("h3")
        self.close_button = self.modal.locator("button[class*='close']")
        self.wishlist_button = self.modal.locator("button[class*='btn-wishlist']")
        self.decrease_quantity_button = self.modal.locator("button[data-spinner='down']")
        self.increase_quantity_button = self.modal.locator("button[data-spinner='up']")
        self.add_to_cart_button = self.modal.locator("button[class*='btn-cart']")
        self.buy_now_button = self.modal.locator("button[class*='btn-buynow']")
        self.compare_button = self.modal.locator("button[class*='btn-compare']")
        self.quantity = self.modal.locator("input[name='quantity']")
        

    def get_title(self):
        return self.title.text_content()
    
    def get_brand(self):
        return self.brand.text_content()

    def is_available(self):
        return self.availability.text_content() == "In Stock"

    def is_unavailable(self):
        return self.availability.text_content() == "Out of Stock"

    def get_price(self):
        return self.price.text_content()
    
    def get_quantity(self):
        return self.quantity.text_content()
    
    def get_product_code(self):
        return self.product_code.text_content()
    
    def close(self):
        self.close_button.click()
    
