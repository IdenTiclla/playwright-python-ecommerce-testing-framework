from playwright.sync_api import Page

class AccountPage:
    URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/account"

    def __init__(self, page: Page):
        self.page = page
        # Locators for common account actions
        self.breadcrumb = ".breadcrumb li.active"
        self.edit_info_link = "a[href*='route=account/edit']"
        self.change_password_link = "a[href*='route=account/password']"
        self.address_book_link = "a[href*='route=account/address']"
        self.wish_list_link = "a[href*='route=account/wishlist']"
        self.order_history_link = "a[href*='route=account/order']"
        self.downloads_link = "a[href*='route=account/download']"
        self.logout_link = "a[href*='route=account/logout']"
        self.return_requests_link = "a[href*='route=account/return']"
        self.newsletter_link = "a[href*='route=account/newsletter']"

    def goto(self):
        self.page.goto(self.URL)

    def is_loaded(self):
        return self.page.locator(self.breadcrumb).is_visible()

    def click_edit_info(self):
        self.page.click(self.edit_info_link)

    def click_change_password(self):
        self.page.click(self.change_password_link)

    def click_address_book(self):
        self.page.click(self.address_book_link)

    def click_wish_list(self):
        self.page.click(self.wish_list_link)

    def click_order_history(self):
        self.page.click(self.order_history_link)

    def click_downloads(self):
        self.page.click(self.downloads_link)

    def click_logout(self):
        self.page.click(self.logout_link)

    def click_return_requests(self):
        self.page.click(self.return_requests_link)

    def click_newsletter(self):
        self.page.click(self.newsletter_link)
