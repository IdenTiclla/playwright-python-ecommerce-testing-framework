from playwright.sync_api import Page, expect

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Search form locators
        self.search_input = page.locator("div#main-header input[placeholder='Search For Products']")
        self.search_button = page.locator("div#main-header div.search-button")
        self.category_dropdown = page.locator("div#main-header button.dropdown-toggle")
        self.search_in_description = page.locator("label[for='description']")
        
        # Search results locators
        self.product_items = page.locator(".product-thumb")
        self.product_titles = page.locator(".product-thumb h4 a")
        self.no_results_message = page.locator("div#product-search p")
        
    def perform_search(self, keyword: str, category: str = "All Categories", search_in_description: bool = False):
        """Execute a search with the given parameters"""
        # Fill search input
        self.search_input.fill(keyword)
        
        # Note: Category selection and description checkbox will be handled on the search results page
        # First submit the search to get to the search page
        self.search_button.click()
        
        # Now handle additional options on search results page
        if category != "All Categories":
            # self.page.wait_for_selector(self.category_dropdown)
            # self.page.select_option(self.category_dropdown, label=category)

            self.category_dropdown.click()
            self.page.wait_for_selector(f"//a[contains(text(), '{category}')]", state="visible")
            self.page.click(f"//a[contains(text(), '{category}')]")

        # Wait for the page to load completely
        self.page.wait_for_load_state("domcontentloaded")
        # Check if the search in description checkbox is visible
        if search_in_description:
            self.search_in_description.wait_for(state="visible")
            self.search_in_description.click()

        # If we changed any options, need to search again
        if category != "All Categories" or search_in_description:
            self.search_button.click()

        
    def get_search_results(self):
        """Return a list of product titles from search results"""
        
        # Wait for the page to load completely
        self.page.wait_for_load_state("domcontentloaded")
        
        # Wait for at least one product title to be visible
        self.product_titles.first.wait_for(state="visible")

        return self.product_titles.all_text_contents()
        
    def get_result_count(self):
        """Return the number of products found"""
        self.page.wait_for_load_state("domcontentloaded")
        return self.product_items.count()
        
    def has_results(self):
        """Check if any results were found"""
        # Wait for the page to load completely
        self.page.wait_for_load_state("domcontentloaded")
        
        # Check if there are any product items
        try:
            # Try to wait for products with a short timeout
            self.product_items.first.wait_for(state="visible", timeout=5000)
            return True
        except:
            # If no products are found, check if the no results message is visible
            try:
                self.no_results_message.wait_for(state="visible", timeout=5000)
                return False
            except:
                # If neither is visible, assume no results
                return False