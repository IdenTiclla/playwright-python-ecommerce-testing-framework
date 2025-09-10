from playwright.sync_api import Page
from components.base_component import BaseComponent
class RelatedProducts(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.related_products = page.locator("div[class*='content-related'] div.product-thumb")
        self.add_to_cart_buttons = "button[class*='btn-cart']"
        self.wishlist_buttons = "button[class*='btn-wishlist']"
        self.compare_buttons = "button[class*='btn-compare']"
        self.quick_view_buttons = "button[class*='quick-view']"

    def get_related_products_count(self):
        """Get the number of related products"""
        return self.related_products.count()

    def get_related_product_name(self, index=0):
        """Get the name of a related product"""
        return self.related_products.locator("h4 a").nth(index).text_content().strip()

    def get_related_product_price(self, index=0):
        """Get the price of a related product"""
        return self.related_products.locator("div.price span").nth(index).text_content()

    def add_product_to_wishlist(self, index=0):
        """Add a product to wishlist"""
        # hover a product by index
        self.related_products.nth(index).hover()
        wishlist_button = self.related_products.locator(self.wishlist_buttons).nth(index)
        
        # Wait for the button to be visible
        wishlist_button.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(200)

        # Click the button
        wishlist_button.click()

    def open_quick_view(self, index=0):
        """Open quick view modal for a product"""
        self.related_products.nth(index).hover()
        quick_view_button = self.related_products.locator(self.quick_view_buttons).nth(index)
        
        # Wait for the button to be visible
        quick_view_button.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(200)
        
        # Click the button
        quick_view_button.click()
    
    def compare_product(self, index=0):
        """Compare a product"""
        self.related_products.nth(index).hover()
        compare_button = self.related_products.locator(self.compare_buttons).nth(index)
        
        # Wait for the button to be visible
        compare_button.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(200)
        
        # Click the button
        compare_button.click()
