from components.search_bar import SearchBar
from components.navbar_horizontal import NavbarHorizontal
from playwright.sync_api import Page
from components.carousel import Carousel

class HomePage:
    URL = "https://ecommerce-playground.lambdatest.io/"

    def __init__(self, page: Page):
        self.page = page
        self.search_bar = SearchBar(page)
        self.navbar_horizontal = NavbarHorizontal(page)
        self.carousel = Carousel(page)

    def goto(self):
        self.page.goto(self.URL)

    def search(self, term):
        self.search_bar.search(term)

    def click_on_my_account(self):
        self.page.click("#my_account")

    def click_on_login(self):
        self.page.click("#login")