class SearchBar:
    SEARCH_INPUT = 'input[name="search"]'
    SEARCH_BUTTON = 'button[type="submit"]'

    def __init__(self, page):
        self.page = page

    def search(self, term):
        self.page.fill(self.SEARCH_INPUT, term)
        self.page.click(self.SEARCH_BUTTON)