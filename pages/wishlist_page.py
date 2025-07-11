from playwright.sync_api import Page
from components.navbar_horizontal import NavbarHorizontal
from components.search_bar import SearchBar
from components.sidebar_navigation import SidebarNavigation
from pages.base_page import BasePage
class WishListPage(BasePage):
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/wishlist"

    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar_horizontal = NavbarHorizontal(page)
        self.search_bar = SearchBar(page)
        self.sidebar_navigation = SidebarNavigation(page)
        
        # Page elements
        self.page_title = self.page.locator("h1")
        self.no_results_message = self.page.locator("h1 + p")
        self.breadcrumb = self.page.locator("nav[aria-label='breadcrumb']")
        self.wishlist_table = self.page.locator("div#content table")
        self.table_headers = self.page.locator("thead tr th")
        self.table_rows = self.page.locator("div#content tbody tr")
        self.continue_button = self.page.locator("div#content a.btn.btn-primary")

        # Table column selectors
        self.product_image_column = self.page.locator("td:nth-child(1)")
        self.product_name_column = self.page.locator("td:nth-child(2)")
        self.model_column = self.page.locator("td:nth-child(3)")
        self.stock_column = self.page.locator("td:nth-child(4)")
        self.price_column = self.page.locator("td:nth-child(5)")
        self.action_column = self.page.locator("td:nth-child(6)")

        # Action buttons in table
        self.add_to_cart_button = self.page.locator("button[title='Add to Cart']")
        self.remove_from_wishlist_button = self.page.locator("a[title='Remove']")

    def goto(self):
        """Navigate to the wishlist page"""
        self.page.goto(self.URL)

    def get_breadcrumb_text(self) -> str:
        """Get the breadcrumb navigation text"""
        return self.breadcrumb.text_content().strip()

    def is_wishlist_table_visible(self) -> bool:
        """Check if the wishlist table is visible"""
        return self.wishlist_table.is_visible()

    def get_table_headers(self) -> list:
        """Get all table header texts"""
        headers = self.table_headers.all()
        return [header.text_content().strip() for header in headers]
    

    def get_wishlist_items_count(self) -> int:
        """Get the number of items in the wishlist"""
        return self.table_rows.count()

    def get_product_details(self, row_index: int = 0) -> dict:
        """Get product details from a specific row (0-based index)"""
        row = self.table_rows.nth(row_index)

        return {
            "image_src": row.locator(f"td:nth-child(1) img").get_attribute("src"),
            "product_name": row.locator(f"td:nth-child(2) a").text_content().strip(),
            "model": row.locator(f"td:nth-child(3)").text_content().strip(),
            "stock_status": row.locator(f"td:nth-child(4)").text_content().strip(),
            "price": row.locator(f"td:nth-child(5)").text_content().strip(),
        }

    def click_product_name(self, row_index: int = 0):
        """Click on product name link to go to product page"""
        row = self.table_rows.nth(row_index)
        row.locator(f"td:nth-child(2) a").click()
    
    def click_product_image(self, row_index: int = 0):
        """Click on product image to go to product page"""
        row = self.table_rows.nth(row_index)
        row.locator(f"td:nth-child(1) img").click()

    def add_to_cart(self, row_index: int = 0):
        """Add product to cart from wishlist"""
        row = self.table_rows.nth(row_index)
        row.locator("button[title='Add to Cart']").click()

    def remove_from_wishlist(self, row_index: int = 0):
        """Remove product from wishlist"""
        row = self.table_rows.nth(row_index)
        row.locator("a[title='Remove']").click()

    def remove_all_from_wishlist(self):
        """Remove all products from wishlist"""
        rows = self.table_rows
        while rows.count() > 0:
            self.remove_from_wishlist(0)
            # Wait for the row to be removed
            self.page.wait_for_timeout(500)

    def click_continue(self):
        """Click the continue button to go back to account page"""
        self.continue_button.click()

    def is_product_in_wishlist(self, product_name: str) -> bool:
        """Check if a specific product is in the wishlist"""
        product_links = self.page.locator(f"{self.product_name_column} a")
        for i in range(product_links.count()):
            if product_name.lower() in product_links.nth(i).text_content().lower():
                return True
        return False

    def get_product_price(self, row_index: int = 0) -> str:
        """Get the price of a product in the wishlist"""
        row = self.table_rows.nth(row_index)
        return row.locator(self.price_column).text_content().strip()

    def get_stock_status(self, row_index: int = 0) -> str:
        """Get the stock status of a product"""
        row = self.table_rows.nth(row_index)
        return row.locator(self.stock_column).text_content().strip()

    def is_add_to_cart_button_enabled(self, row_index: int = 0) -> bool:
        """Check if add to cart button is enabled for a product"""
        row = self.table_rows.nth(row_index)
        button = row.locator(self.add_to_cart_button)
        return button.is_enabled() if button.is_visible() else False
    
    def get_no_results_message(self) -> str:
        """Get the no results message"""
        return self.no_results_message.text_content().strip() if self.no_results_message.is_visible() else ""


    def wait_for_page_load(self):
        """Wait for the wishlist page to fully load"""
        self.page.wait_for_load_state("domcontentloaded")

    def get_page_title(self) -> str:
        """Get the page title"""
        return self.page_title.text_content().strip()
        # return self.page.locator(self.page_title).text_content().strip()