from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage
class TopProducts(BasePage):
    def __init__(self, page: Page):
        self.page = page
        self.section = self.page.locator("//h3[contains(text(), 'Top Products')]/parent::div/parent::div")
        self.product_items = self.page.locator("//h3[contains(text(), 'Top Products')]/parent::div/parent::div//div[contains(@class, 'product-thumb image-top')]")
        self.cart_buttons = "button[class*='btn-cart']"
        self.wishlist_buttons = "button[class*='btn-wishlist']"
        self.compare_buttons = f"{self.product_items} button[class*='btn-compare']"
        self.quick_view_buttons = "button[class*='quick-view']"

    def is_visible(self):
        return self.page.locator(self.section).is_visible()

    def get_product_titles(self):
        return self.product_items.locator("h4 a").all_text_contents()

    def click_product_by_title(self, title: str):
        self.product_items.locator(f"h4 a:has-text('{title}')").first.click()

    def hover_over_top_product(self, index=0):
        self.product_items.nth(index).hover()

    def scroll_to_top_products(self):
        """Scrolls to the top products section."""
        self.section.scroll_into_view_if_needed()

    def add_product_to_cart(self, index=0):
        # Ensure section is visible using expect
        self.scroll_to_top_products()
        # self.page.wait_for_timeout(500)
        self.page.wait_for_load_state("networkidle", timeout=5000)

        
        # Hover over product to make button accessible
        # self.product_items.nth(index).scroll_into_view_if_needed()
        self.hover_over_top_product(index)
        
        # Get cart button within this specific product
        cart_button = self.product_items.nth(index).locator("button[class*='btn-cart']")

        cart_button.click()

    def add_product_to_wishlist(self, index=0):
        # self.page.locator(self.wishlist_buttons).nth(index).click()
        self.scroll_to_top_products()
        self.page.wait_for_load_state("networkidle", timeout=5000)

        self.hover_over_top_product(index)

        wishlist_button = self.product_items.nth(index).locator("button[class*='btn-wishlist']")
        wishlist_button.click()
            
    def show_quick_view(self, index=0):
        self.scroll_to_top_products()
        self.page.wait_for_load_state("networkidle", timeout=5000)

        self.hover_over_top_product(index)

        quick_view_button = self.product_items.nth(index).locator("button[class*='quick-view']")    
        quick_view_button.click()
        


    def add_product_to_compare(self, index=0):
        self.product_items.locator(self.compare_buttons).nth(index).click()

    def get_product_name(self, index=0):
        return self.product_items.locator("h4 a").nth(index).text_content().strip()
    
    def get_product_price(self, index=0):
        product_price = self.product_items.locator("div.price span").nth(index).text_content().strip("$")
        return round(float(product_price), 2)
    