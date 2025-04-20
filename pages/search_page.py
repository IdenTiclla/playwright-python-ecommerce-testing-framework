from playwright.sync_api import Page, expect

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Search form locators
        self.search_input = "div#main-header input[placeholder='Search For Products']"
        self.search_button = "div#main-header div.search-button"
        self.category_dropdown = "div#main-header button.dropdown-toggle"
        self.search_in_description = "input[name='description']"
        
        # Search results locators
        self.product_items = ".product-thumb"
        self.product_titles = ".product-thumb h4 a"
        self.no_results_message = "div#product-search p"
        
    def perform_search(self, keyword: str, category: str = "All Categories", search_in_description: bool = False):
        """Execute a search with the given parameters"""
        # Fill search input
        self.page.fill(self.search_input, keyword)
        
        # Note: Category selection and description checkbox will be handled on the search results page
        # First submit the search to get to the search page
        self.page.click(self.search_button)
        
        # Now handle additional options on search results page
        if category != "All Categories":
            # self.page.wait_for_selector(self.category_dropdown)
            # self.page.select_option(self.category_dropdown, label=category)

            self.page.click(self.category_dropdown)
            self.page.wait_for_selector(f"//a[contains(text(), '{category}')]", state="visible")
            self.page.click(f"//a[contains(text(), '{category}')]")

        if search_in_description:
            self.page.wait_for_selector(self.search_in_description)
            self.page.check(self.search_in_description)
            
        # If we changed any options, need to search again
        if category != "All Categories" or search_in_description:
            self.page.click('input[value="Search"]')
        
    def get_search_results(self):
        """Return a list of product titles from search results"""
        self.page.wait_for_selector(self.product_titles)
        return self.page.locator(self.product_titles).all_text_contents()
        
    def get_result_count(self):
        """Return the number of products found"""
        self.page.wait_for_selector(self.product_items)
        return self.page.locator(self.product_items).count()
        
    def has_results(self):
        """Check if any results were found"""
        # Wait for either products or no results message
        self.page.wait_for_selector(f"{self.product_items}, {self.no_results_message}")
        return self.page.locator(self.product_items).count() > 0