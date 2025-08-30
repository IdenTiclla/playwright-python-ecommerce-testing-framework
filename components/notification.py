from playwright.sync_api import Page, expect

class Notification:
    def __init__(self, page: Page):
        self.page = page
        self.container = self.page.locator("div#notification-box-top")
        self.title = self.page.locator("div#notification-box-top div[class*='toast-header'] span[class='mr-auto']")
        self.close_button = self.page.locator("div#notification-box-top div[class*='toast-header'] button")
        self.message = self.page.locator("div#notification-box-top div[class*='toast-body'] p")
        self.login_button = self.page.locator("div#notification-box-top div[class*='toast-body'] div[class='form-row'] a[href*='login']")
        self.register_button = self.page.locator("div#notification-box-top div[class*='toast-body'] div[class='form-row'] a[href*='register']")
        self.view_cart_button = self.page.locator("div#notification-box-top div[class='form-row'] a[href*='checkout/cart']")
        self.checkout_button = self.page.locator("div#notification-box-top div[class='form-row'] a[href*='checkout/checkout']")
        
    def close(self):
        """Close the notification"""
        if self.is_visible():
            # Try multiple strategies to close the notification
            try:
                # First attempt: normal click
                self.close_button.click()
                # Wait a bit for the animation
                self.page.wait_for_timeout(500)
                
                # Check if it's hidden, if not try force click
                if self.is_visible():
                    self.close_button.click(force=True)
                    self.page.wait_for_timeout(500)
                
                # Give it time to hide with a more lenient check
                self.page.wait_for_function(
                    "() => !document.querySelector('div#notification-box-top') || document.querySelector('div#notification-box-top').offsetParent === null",
                    timeout=10000
                )
            except Exception:
                # If all else fails, just wait and don't enforce hiding
                self.page.wait_for_timeout(1000)

    def is_notification_visible(self):
        return self.container.is_visible()

    def get_title_text(self):
        return self.title.inner_text()

    def is_visible(self):
        return self.container.is_visible()
    
    def get_message_text(self):
        return self.message.inner_text()
    
    def get_login_button_text(self):
        return self.login_button.inner_text()
    
    def get_register_button_text(self):
        return self.register_button.inner_text()
    
    def click_on_view_cart_button(self):
        self.view_cart_button.click()
    
    def wait_until_hidden(self, timeout=10000):
        """Wait until the notification is completely hidden"""
        expect(self.container).to_be_hidden(timeout=timeout)
    
    def clear_all_notifications(self):
        """Clear any existing notifications before starting tests"""
        max_attempts = 3
        for attempt in range(max_attempts):
            if not self.is_visible():
                break
            try:
                self.close()
                # Give it a moment to process
                self.page.wait_for_timeout(1000)
            except Exception:
                # If closing fails, just wait a bit and continue
                self.page.wait_for_timeout(1000)
                continue
        