from playwright.sync_api import Page
from components.navbar_horizontal import NavbarHorizontal
from components.search_bar import SearchBar


class WishlistPage:
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/wishlist"

    def __init__(self, page: Page):
        self.page = page
        self.navbar_horizontal = NavbarHorizontal(page)
        self.search_bar = SearchBar(page)
        
        # Page elements
        self.page_title = "h1"
        self.no_results_message = "h1 + p"
        self.breadcrumb = "nav[aria-label='breadcrumb']"
        self.wishlist_table = "table"
        self.table_headers = "thead tr th"
        self.table_rows = "tbody tr"
        self.continue_button = "a.btn.btn-primary"
        
        # Table column selectors
        self.product_image_column = "td:nth-child(1)"
        self.product_name_column = "td:nth-child(2)"
        self.model_column = "td:nth-child(3)"
        self.stock_column = "td:nth-child(4)"
        self.price_column = "td:nth-child(5)"
        self.action_column = "td:nth-child(6)"
        
        # Action buttons in table
        self.add_to_cart_button = "button[title='Add to Cart']"
        self.remove_from_wishlist_button = "a[title='Remove']"
        
        # Sidebar navigation
        self.sidebar = "aside"
        self.sidebar_links = "aside a"
        self.my_account_link = "a[href*='account/account']"
        self.edit_account_link = "a[href*='account/edit']"
        self.password_link = "a[href*='account/password']"
        self.address_book_link = "a[href*='account/address']"
        self.wishlist_link = "a[href*='account/wishlist']"
        self.order_history_link = "a[href*='account/order']"
        self.logout_link = "a[href*='account/logout']"

    def goto(self):
        """Navigate to the wishlist page"""
        self.page.goto(self.URL)

    def get_breadcrumb_text(self) -> str:
        """Get the breadcrumb navigation text"""
        return self.page.locator(self.breadcrumb).text_content().strip()

    def is_wishlist_table_visible(self) -> bool:
        """Check if the wishlist table is visible"""
        return self.page.locator(self.wishlist_table).is_visible()

    def get_table_headers(self) -> list:
        """Get all table header texts"""
        headers = self.page.locator(self.table_headers).all()
        return [header.text_content().strip() for header in headers]
    

    def get_wishlist_items_count(self) -> int:
        """Get the number of items in the wishlist"""
        return self.page.locator(self.table_rows).count()

    def get_product_details(self, row_index: int = 0) -> dict:
        """Get product details from a specific row (0-based index)"""
        row = self.page.locator(self.table_rows).nth(row_index)
        
        return {
            "image_src": row.locator(f"{self.product_image_column} img").get_attribute("src"),
            "product_name": row.locator(f"{self.product_name_column} a").text_content().strip(),
            "model": row.locator(self.model_column).text_content().strip(),
            "stock_status": row.locator(self.stock_column).text_content().strip(),
            "price": row.locator(self.price_column).text_content().strip(),
        }

    def click_product_name(self, row_index: int = 0):
        """Click on product name link to go to product page"""
        row = self.page.locator(self.table_rows).nth(row_index)
        row.locator(f"{self.product_name_column} a").click()

    def click_product_image(self, row_index: int = 0):
        """Click on product image to go to product page"""
        row = self.page.locator(self.table_rows).nth(row_index)
        row.locator(f"{self.product_image_column} a").click()

    def add_to_cart(self, row_index: int = 0):
        """Add product to cart from wishlist"""
        row = self.page.locator(self.table_rows).nth(row_index)
        row.locator(self.add_to_cart_button).click()

    def remove_from_wishlist(self, row_index: int = 0):
        """Remove product from wishlist"""
        row = self.page.locator(self.table_rows).nth(row_index)
        row.locator(self.remove_from_wishlist_button).click()

    def click_continue(self):
        """Click the continue button to go back to account page"""
        self.page.locator(self.continue_button).click()

    def is_product_in_wishlist(self, product_name: str) -> bool:
        """Check if a specific product is in the wishlist"""
        product_links = self.page.locator(f"{self.product_name_column} a")
        for i in range(product_links.count()):
            if product_name.lower() in product_links.nth(i).text_content().lower():
                return True
        return False

    def get_product_price(self, row_index: int = 0) -> str:
        """Get the price of a product in the wishlist"""
        row = self.page.locator(self.table_rows).nth(row_index)
        return row.locator(self.price_column).text_content().strip()

    def get_stock_status(self, row_index: int = 0) -> str:
        """Get the stock status of a product"""
        row = self.page.locator(self.table_rows).nth(row_index)
        return row.locator(self.stock_column).text_content().strip()

    def is_add_to_cart_button_enabled(self, row_index: int = 0) -> bool:
        """Check if add to cart button is enabled for a product"""
        row = self.page.locator(self.table_rows).nth(row_index)
        button = row.locator(self.add_to_cart_button)
        return button.is_enabled() if button.is_visible() else False

    # Sidebar navigation methods
    def click_my_account(self):
        """Navigate to My Account page"""
        self.page.locator(self.my_account_link).click()

    def click_edit_account(self):
        """Navigate to Edit Account page"""
        self.page.locator(self.edit_account_link).click()

    def click_password(self):
        """Navigate to Password page"""
        self.page.locator(self.password_link).click()

    def click_address_book(self):
        """Navigate to Address Book page"""
        self.page.locator(self.address_book_link).click()

    def click_order_history(self):
        """Navigate to Order History page"""
        self.page.locator(self.order_history_link).click()

    def logout(self):
        """Logout from the account"""
        self.page.locator(self.logout_link).click()

    def wait_for_page_load(self):
        """Wait for the wishlist page to fully load"""
        self.page.wait_for_load_state("domcontentloaded")
        # self.page.locator(self.page_title).wait_for(state="visible") 