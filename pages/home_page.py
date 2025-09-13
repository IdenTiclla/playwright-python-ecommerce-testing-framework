from playwright.sync_api import Page
from components.carousel import MainCarousel
from components.top_products import TopProducts
from components.top_collection import TopCollection
from components.quick_view_modal import QuickViewModal
from components.notification import Notification
from components.cart_panel import CartPanel
from components.articles import Articles
from pages.base_page import BasePage
from components.header_actions import HeaderActions
from utils.config import BASE_URL

class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.carousel = MainCarousel(page)
        self.top_products = TopProducts(page)
        self.top_collection = TopCollection(page)
        self.quick_view_modal = QuickViewModal(page)
        self.notification = Notification(page)
        self.cart_panel = CartPanel(page)
        self.header_actions = HeaderActions(page)
        self.articles = Articles(page)


    def goto(self):
        self.page.goto(f"{BASE_URL}/")

    def search(self, term):
        self.search_bar.search(term)

    def click_on_compare_button(self):
        self.compare_button.click()

    def click_on_wishlist_button(self):
        self.wishlist_button.click()

    def click_on_my_cart_button(self):
        self.cart_button.scroll_into_view_if_needed()
        self.cart_button.click()