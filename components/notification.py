from playwright.sync_api import Page

class Notification:
    def __init__(self, page: Page):
        self.page = page
        self.container = "div#notification-box-top"
        self.title = f"{self.container} div[class*='toast-header'] span[class='mr-auto']"
        self.close_button = f"{self.container} div[class*='toast-header'] button"
        self.message = f"{self.container} div[class*='toast-body'] p"
        self.login_button = f"{self.container} div[class*='toast-body'] div[class='form-row'] a[href*='login']"
        self.register_button = f"{self.container} div[class*='toast-body'] div[class='form-row'] a[href*='register']"
        
    def close(self):
        self.page.locator(self.close_button).click()

    def get_title_text(self):
        return self.page.locator(self.title).inner_text()
        
    def is_visible(self):
        return self.page.locator(self.container).is_visible()
    
    def get_message_text(self):
        return self.page.locator(self.message).inner_text()
    
    def get_login_button_text(self):
        return self.page.locator(self.login_button).inner_text()
    
    def get_register_button_text(self):
        return self.page.locator(self.register_button).inner_text()