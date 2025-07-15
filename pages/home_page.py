from playwright.sync_api import Page
from components.carousel import Carousel
from components.top_products import TopProducts
from components.quick_view_modal import QuickViewModal
from components.notification import Notification
from pages.base_page import BasePage
from components.header_actions import HeaderActions

class HomePage(BasePage):
    URL = "https://ecommerce-playground.lambdatest.io/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.carousel = Carousel(page)
        self.top_products = TopProducts(page)
        self.quick_view_modal = QuickViewModal(page)
        self.notification = Notification(page)
        self.header_actions = HeaderActions(page)


    def goto(self):
        self.page.goto(self.URL)

    def search(self, term):
        self.search_bar.search(term)

    def click_on_compare_button(self):
        self.compare_button.click()

    def click_on_wishlist_button(self):
        self.wishlist_button.click()

    def click_on_my_cart_button(self):
        self.cart_button.click()