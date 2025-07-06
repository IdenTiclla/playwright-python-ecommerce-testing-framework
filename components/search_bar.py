class SearchBar:
    SEARCH_INPUT = 'input[name="search"]'
    SEARCH_BUTTON = 'button[type="submit"]'

    # implement a method to perform a search with category, search in description, search in subcategories

    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("div#main-header input[name='search']")
        self.search_button = page.locator("div#main-header button[type='submit']")
        self.search_category_dropdown = page.locator("div#main-header button.dropdown-toggle")
        self.category_dropdown_options = page.locator("div#main-header .dropdown-menu a.dropdown-item")

    def search(self, term):
        self.search_input.fill(term)
        self.search_button.click()

    def select_category(self, category):
        # Open the dropdown
        self.search_category_dropdown.click()
        
        # Use Playwright's auto-waiting - it will wait for the element to be actionable
        category_option = self.category_dropdown_options.filter(has_text=category)
        
        # Click on the category - Playwright will auto-wait for it to be clickable
        category_option.click()
