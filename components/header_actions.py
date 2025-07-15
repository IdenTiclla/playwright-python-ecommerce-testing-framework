from playwright.sync_api import Page

class HeaderActions:
    def __init__(self, page: Page):
        self.page = page
        self.compare_button = page.locator("div#main-header a[href*='route=product/compare']")
        self.wishlist_button = page.locator("div#main-header a[href*='route=account/wishlist']")
        self.cart_button = page.locator("#main-header #entry_217820 > .entry-widget.widget-cart")

    def click_on_compare_button(self):
        self.compare_button.click()

    def click_on_wishlist_button(self):
        self.wishlist_button.click()

    def click_on_cart_button(self):
        self.cart_button.click()

    def get_cart_count(self):
        return self.cart_button.locator("span.cart-item-total").text_content()