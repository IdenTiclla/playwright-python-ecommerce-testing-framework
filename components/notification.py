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
        self.close_button.click()

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
        