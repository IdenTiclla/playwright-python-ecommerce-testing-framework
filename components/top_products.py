from playwright.sync_api import Page
from playwright.sync_api import expect

class TopProducts:
    def __init__(self, page: Page):
        self.page = page
        self.section = "div#entry_217977 > div[class*='entry-section']"
        self.product_cards = "div#entry_217977 .product-thumb"
        self.product_titles = f"{self.product_cards} h4 a"
        self.product_prices = "div#entry_217977 .product-thumb div.price span"
        self.cart_buttons = "button[class*='btn-cart']"
        self.wishlist_buttons = "button[class*='btn-wishlist']"
        self.compare_buttons = f"{self.product_cards} button[class*='btn-compare']"
        self.quick_view_buttons = "button[class*='quick-view']"

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
        # Ensure section is visible using expect
        self.scroll_to_top_products()
        self.page.wait_for_load_state("networkidle")

        expect(self.page.locator(self.section)).to_be_visible()
        
        # Get product card and ensure it's visible
        product_card = self.page.locator(self.product_cards).nth(index)
        expect(product_card).to_be_visible()
        
        # Hover over product to make button accessible
        product_card.hover()
        
        # Get cart button within this specific product
        cart_button = product_card.locator(self.cart_buttons)
        
        # Playwright auto-waits for the button to be visible and enabled
        expect(cart_button).to_be_visible()
        expect(cart_button).to_be_enabled()
        
        # click the button
        cart_button.click()

    def add_product_to_wishlist(self, index=0):
        # self.page.locator(self.wishlist_buttons).nth(index).click()
        self.scroll_to_top_products()
        self.page.wait_for_load_state("networkidle")

        product_card = self.page.locator(self.product_cards).nth(index)
        expect(product_card).to_be_visible(timeout=5000)

        wishlist_button = product_card.locator(self.wishlist_buttons)
        expect(wishlist_button).to_be_visible(timeout=5000)
        expect(wishlist_button).to_be_enabled(timeout=5000)

        self.page.wait_for_timeout(500)
        product_card.hover()

        try:
            wishlist_button.click()
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception as e:
            self.page.evaluate("(button) => button.click()", wishlist_button)
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
    def show_quick_view(self, index=0):
        self.scroll_to_top_products()
        self.page.wait_for_load_state("networkidle")

        product_card = self.page.locator(self.product_cards).nth(index)
        product_card.scroll_into_view_if_needed()
        expect(product_card).to_be_visible(timeout=5000)

        # Add explicit waits to avoid potential race conditions
        self.page.wait_for_timeout(500)
        product_card.hover()

        quick_view_button = product_card.locator(self.quick_view_buttons)    
        expect(quick_view_button).to_be_visible(timeout=5000)
        expect(quick_view_button).to_be_enabled(timeout=5000)

        self.page.wait_for_timeout(500)

        try:
            quick_view_button.click()
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception as e:
            self.page.evaluate("(button) => button.click()", quick_view_button)
            self.page.wait_for_load_state("networkidle", timeout=5000)

    def add_product_to_compare(self, index=0):
        self.page.locator(self.compare_buttons).nth(index).click()


    def get_product_name(self, index=0):
        return self.page.locator(self.product_titles).nth(index).text_content().strip()
    
    def get_product_price(self, index=0):
        product_price = self.page.locator(self.product_prices).nth(index).text_content().strip("$")
        return round(float(product_price), 2)
    