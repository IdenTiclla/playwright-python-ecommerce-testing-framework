from playwright.sync_api import Page, expect
from components.search_bar import SearchBar
from pages.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, page: Page):
        self.page = page

        # components
        self.search_bar = SearchBar(page)
        
        # Search form locators
        self.search_input = page.locator("div#main-header input[placeholder='Search For Products']")
        self.search_button = page.locator("div#main-header div.search-button")
        self.category_dropdown = page.locator("div#main-header button.dropdown-toggle")
        self.search_in_description = page.locator("label[for='description']")

        self.sort_by_select = page.locator("select#input-sort-212464")
        
        # Search results locators
        self.product_items = page.locator(".product-thumb")
        self.product_titles = page.locator(".product-thumb h4 a")
        self.no_results_message = page.locator("div#product-search p")
        
    def perform_search(self, keyword: str, category: str = "All Categories", search_in_description: bool = False):
        """Execute a search with the given parameters"""
        # Fill search input and click search - Playwright auto-waits for elements
        self.search_input.fill(keyword)
        self.search_button.click()
        
        # Handle additional options on search results page if needed
        if category != "All Categories":
            self.search_bar.select_category(category)

        # Check if search in description checkbox is available (optional element)
        if search_in_description:
            # Use is_visible() to check without throwing exceptions
            if self.search_in_description.is_visible():
                self.search_in_description.click()
            else:
                print("Warning: Search in description checkbox not found or not visible")

        # Re-search if we changed any options
        if category != "All Categories" or search_in_description:
            self.search_button.click()

        
    def get_search_results(self):
        """Return a list of product titles from search results"""
        # Playwright auto-waits for elements when using all_text_contents()
        return self.product_titles.all_text_contents()
        
    def get_result_count(self):
        """Return the number of products found"""
        # count() automatically waits for elements to be attached to DOM
        return self.product_items.count()
        
    def has_results(self):
        """Check if any results were found"""
        # Use is_visible() with short timeout to check for results efficiently
        if self.product_items.first.is_visible():
            return True
        # If no products are visible, we have no results
        return False
            

    def get_product_prices(self):
        """Return a list of product prices from search results"""
        # Playwright auto-waits for elements when using all_text_contents()
        price_locator = self.product_items.locator("div.price")
        prices_str = price_locator.all_text_contents()
        prices_float = [float(price.replace("$", "")) for price in prices_str]
        return prices_float
    
            
    def select_sort_by(self, sort_by: str):
        """Select a sort by option"""
        # select_option() auto-waits and triggers change events
        self.sort_by_select.select_option(sort_by)
        # Wait for network activity to settle after sorting
        self.page.wait_for_load_state("networkidle")
            
    def sort_by_price_low_to_high(self):
        """Sort the search results by price low to high"""
        self.select_sort_by("Price (Low > High)")

    def sort_by_price_high_to_low(self):
        """Sort the search results by price high to low"""
        self.select_sort_by("Price (High > Low)")

    def check_if_sorted_by_price_low_to_high(self):
        """Check if the search results are sorted by price low to high"""
        # Wait for the first product to be visible (ensures sorting is complete)
        expect(self.product_items.first).to_be_visible()
        prices = self.get_product_prices()
        return prices == sorted(prices)
    
    def check_if_sorted_by_price_high_to_low(self):
        """Check if the search results are sorted by price high to low"""
        # Wait for the first product to be visible (ensures sorting is complete)
        expect(self.product_items.first).to_be_visible()
        prices = self.get_product_prices()
        return prices == sorted(prices, reverse=True)
    
    def get_product_name(self, index: int):
        """Get the name of a product"""
        return self.product_items.nth(index).locator("h4 a").text_content()
    
    def get_product_price(self, index: int):
        """Get the price of a product"""
        price = self.product_items.nth(index).locator("div.price").text_content() 
        return round(float(price.replace("$", "")), 2)
    

    def hover_over_product(self, index: int):
        """Hover over a product"""
        self.product_items.nth(index).hover()
    
    def add_product_to_cart(self, index: int):
        """Add a product to the cart"""
        self.hover_over_product(index)
        self.product_items.nth(index).locator("button.btn-cart").click()

    