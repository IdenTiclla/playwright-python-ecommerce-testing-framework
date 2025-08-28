from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage

class TopCollection(BasePage):
    def __init__(self, page: Page):
        self.page = page
        # Based on the pattern from TopProducts, we'll try multiple selector strategies
        # First try: Look for a specific entry ID pattern like TopProducts uses
        self.section = self.page.locator("div#mz-product-listing-39218404")
        
        # Fallback: Use a more specific approach targeting the actual section
        if not self.section.count():
            self.section = self.page.locator("div:has-text('TOP COLLECTION')").filter(has=self.page.locator(".nav-tabs, .product-thumb")).first
        
        # Product items within the section
        self.product_items = self.page.locator("div#mz-product-listing-39218404 div.product-thumb")
        
        # Tab selectors - these are the POPULAR, LATEST, BEST SELLER tabs
        # Try multiple approaches for finding tabs
        self.popular_tab = self.section.locator("a:has-text('POPULAR'), .nav-link:has-text('POPULAR'), [data-tab='popular']").first
        self.latest_tab = self.section.locator("a:has-text('LATEST'), .nav-link:has-text('LATEST'), [data-tab='latest']").first
        self.best_seller_tab = self.section.locator("a:has-text('BEST SELLER'), .nav-link:has-text('BEST SELLER'), [data-tab='bestseller']").first
        
        # Product action buttons (similar to TopProducts)
        self.cart_buttons = "button[class*='btn-cart']"
        self.wishlist_buttons = "button[class*='btn-wishlist']"
        self.compare_buttons = "button[class*='btn-compare']"
        self.quick_view_buttons = "button[class*='quick-view']"

    def is_visible(self):
        """Check if the Top Collection section is visible"""
        return self.section.is_visible()

    def scroll_to_top_collection(self):
        """Scrolls to the top collection section."""
        self.section.scroll_into_view_if_needed()

    def click_popular_tab(self):
        """Click on the POPULAR tab"""
        self.scroll_to_top_collection()
        self.popular_tab.click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def click_latest_tab(self):
        """Click on the LATEST tab"""
        self.scroll_to_top_collection()
        self.latest_tab.click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def click_best_seller_tab(self):
        """Click on the BEST SELLER tab"""
        self.scroll_to_top_collection()
        self.best_seller_tab.click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def get_active_tab(self):
        """Get the currently active tab text"""
        active_tab = self.section.locator("a.active, .nav-link.active").first
        if active_tab.is_visible():
            return active_tab.text_content().strip()
        return None

    def get_product_titles(self):
        """Get all product titles in the current tab"""
        return self.product_items.locator("h4 a").all_text_contents()

    def click_product_by_title(self, title: str):
        """Click on a product by its title"""
        self.product_items.locator(f"h4 a:has-text('{title}')").first.click()

    def hover_over_product(self, index=0):
        """Hover over a product to reveal action buttons"""
        self.product_items.nth(index).hover()

    def add_product_to_cart(self, index=0):
        """Add a product to cart by index"""
        # Ensure section is visible
        self.scroll_to_top_collection()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        
        # Hover over product to make button accessible
        self.hover_over_product(index)
        
        # Wait a bit for the hover effect to take place
        self.page.wait_for_timeout(500)
        
        # Get cart button within this specific product
        cart_button = self.product_items.nth(index).locator("button[class*='btn-cart']")
        
        # Try JavaScript click if regular click fails
        try:
            cart_button.click(timeout=3000)
        except:
            # Use JavaScript click as fallback
            cart_button.evaluate("element => element.click()")

    def add_product_to_wishlist(self, index=0):
        """Add a product to wishlist by index"""
        self.scroll_to_top_collection()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        
        self.hover_over_product(index)
        self.page.wait_for_timeout(500)
        
        wishlist_button = self.product_items.nth(index).locator("button[class*='btn-wishlist']")
        try:
            wishlist_button.click(timeout=3000)
        except:
            wishlist_button.evaluate("element => element.click()")

    def show_quick_view(self, index=0):
        """Show quick view modal for a product"""
        self.scroll_to_top_collection()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        
        self.hover_over_product(index)
        self.page.wait_for_timeout(500)
        
        quick_view_button = self.product_items.nth(index).locator("button[class*='quick-view']")
        try:
            quick_view_button.click(timeout=3000)
        except:
            quick_view_button.evaluate("element => element.click()")

    def add_product_to_compare(self, index=0):
        """Add a product to compare list"""
        self.scroll_to_top_collection()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        
        self.hover_over_product(index)
        self.page.wait_for_timeout(500)
        
        compare_button = self.product_items.nth(index).locator("button[class*='btn-compare']")
        try:
            compare_button.click(timeout=3000)
        except:
            compare_button.evaluate("element => element.click()")

    def get_product_name(self, index=0):
        """Get product name by index"""
        return self.product_items.locator("h4 a").nth(index).text_content().strip()
    
    def get_product_price(self, index=0):
        """Get product price by index"""
        product_price = self.product_items.locator("div.price span").nth(index).text_content().strip("$")
        return round(float(product_price), 2)

    def get_product_count(self):
        """Get the number of products currently displayed"""
        return self.product_items.count()

    def switch_to_tab_and_add_to_cart(self, tab_name: str, product_index=0):
        """
        Switch to a specific tab and add a product to cart
        tab_name: 'POPULAR', 'LATEST', or 'BEST SELLER'
        """
        tab_name = tab_name.upper()
        
        if tab_name == 'POPULAR':
            self.click_popular_tab()
        elif tab_name == 'LATEST':
            self.click_latest_tab()
        elif tab_name == 'BEST SELLER':
            self.click_best_seller_tab()
        else:
            raise ValueError(f"Invalid tab name: {tab_name}. Use 'POPULAR', 'LATEST', or 'BEST SELLER'")
        
        # Wait for content to load after tab switch
        self.page.wait_for_timeout(1000)
        
        # Add product to cart
        self.add_product_to_cart(product_index)