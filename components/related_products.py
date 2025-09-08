from playwright.sync_api import Page
from components.base_component import BaseComponent

class RelatedProducts(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.related_products = page.locator("div[class*='content-related'] div.product-thumb")

    def get_related_products_count(self):
        """Get the number of related products"""
        return self.related_products.count()