from playwright.sync_api import Page

class TopProducts:
    def __init__(self, page: Page):
        self.page = page
        self.section = "div#entry_217977 > div[class*='entry-section']"
        self.product_cards = "div#entry_217977 .product-thumb"
        self.product_titles = f"{self.product_cards} h4 a"
        self.cart_buttons = f"{self.product_cards} button[class*='btn-cart']"
        self.wishlist_buttons = f"{self.product_cards} button[class*='btn-wishlist']"
        self.compare_buttons = f"{self.product_cards} button[class*='btn-compare']"

    def is_visible(self):
        return self.page.locator(self.section).is_visible()

    def get_product_titles(self):
        return self.page.locator(self.product_titles).all_text_contents()

    def click_product_by_title(self, title: str):
        self.page.locator(f"{self.product_titles}:has-text('{title}')").first.click()

    def scroll_to_top_products(self):
        """Scrolls to the top products section."""
        self.page.locator(self.section).scroll_into_view_if_needed()

    def add_product_to_cart(self, index=0):
        """Adds the product at the given index to the cart."""
        if index < 0:
            raise ValueError("Index must be a non-negative integer.")
        
        self.page.locator(self.product_cards).nth(index).hover()
        self.page.locator(self.cart_buttons).nth(index).click()

    def add_product_to_wishlist(self, index=0):
        self.page.locator(self.wishlist_buttons).nth(index).click()

    def add_product_to_compare(self, index=0):
        self.page.locator(self.compare_buttons).nth(index).click()
