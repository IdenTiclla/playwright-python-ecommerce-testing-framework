from playwright.sync_api import Page


class SidebarNavigation:
    def __init__(self, page: Page):
        self.page = page
        # Sidebar navigation
        self.sidebar = "aside"
        self.sidebar_links = f"{self.sidebar} a"
        self.login_link = f"{self.sidebar} a[href*='account/login']"
        self.register_link = f"{self.sidebar} a[href*='account/register']"
        self.forgotten_password_link = f"{self.sidebar} a[href*='account/forgotten']"
        self.my_account_link = f"{self.sidebar} a[href*='account/account']"
        self.edit_account_link = f"{self.sidebar} a[href*='account/edit']"
        self.password_link = f"{self.sidebar} a[href*='account/password']"
        self.address_book_link = f"{self.sidebar} a[href*='account/address']"
        self.wishlist_link = f"{self.sidebar} a[href*='account/wishlist']"
        self.notification_link = f"{self.sidebar} a[href*='account/notification']"
        self.order_history_link = f"{self.sidebar} a[href*='account/order']"
        self.download_link = f"{self.sidebar} a[href*='account/download']"
        self.recurring_payments_link = f"{self.sidebar} a[href*='account/recurring']"
        self.reward_points_link = f"{self.sidebar} a[href*='account/reward']"
        self.returns_link = f"{self.sidebar} a[href*='account/return']"
        self.transactions_link = f"{self.sidebar} a[href*='account/transaction']"
        self.newsletter_link =  f"{self.sidebar} a[href*='account/newsletter']"
        self.logout_link = f"{self.sidebar} a[href*='account/logout']"

    def click_login_option(self):
        """Click on the login option"""
        self.page.locator(self.login_link).click()

    def click_register_option(self):
        """Click on the register option"""
        self.page.locator(self.register_link).click()

    def click_forgotten_password_option(self):
        """Click on the forgotten password option"""
        self.page.locator(self.forgotten_password_link).click()

    def click_notification_option(self):
        """Click on the notification option"""
        self.page.locator(self.notification_link).click()

    def click_download_option(self):
        """Click on the download option"""
        self.page.locator(self.download_link).click()

    def click_recurring_payments_option(self):
        """Click on the recurring payments option"""
        self.page.locator(self.recurring_payments_link).click()

    def click_reward_points_option(self):
        """Click on the reward points option"""
        self.page.locator(self.reward_points_link).click()

    def click_returns_option(self):
        """Click on the returns option"""
        self.page.locator(self.returns_link).click()

    def click_transactions_option(self):
        """Click on the transactions option"""
        self.page.locator(self.transactions_link).click()

    def click_newsletter_option(self):
        """Click on the newsletter option"""
        self.page.locator(self.newsletter_link).click()

    def click_edit_account_option(self):
        """Click on the edit account option"""
        self.page.locator(self.edit_account_link).click()

    def click_password_option(self):
        """Click on the password option"""
        self.page.locator(self.password_link).click()

    def click_address_book_option(self):
        """Click on the address book option"""
        self.page.locator(self.address_book_link).click()

    def click_wishlist_option(self):
        """Click on the wishlist option"""
        self.page.locator(self.wishlist_link).click()

    def click_order_history_option(self):
        """Click on the order history option"""
        self.page.locator(self.order_history_link).click()

    def click_logout_option(self):
        """Click on the logout option"""
        self.page.locator(self.logout_link).click()

    def click_my_account_option(self):
        """Click on the my account option"""
        self.page.locator(self.my_account_link).click()

    def get_quantity_of_sidebar_links(self) -> int:
        """Get the quantity of sidebar links"""
        return len(self.page.locator(self.sidebar_links).all())


    def get_sidebar_links(self) -> list[str]:
        """Get all sidebar links"""
        return self.page.locator(self.sidebar_links).all_text_contents()

    def is_sidebar_visible(self) -> bool:
        """Check if the sidebar is visible"""
        return self.page.locator(self.sidebar).is_visible()
    