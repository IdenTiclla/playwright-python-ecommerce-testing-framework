from playwright.sync_api import Page
from components.base_component import BaseComponent


class AuthorContent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.author_image = page.locator("div[class*='content-author '] a[class*='flex-shrink']")
        self.author_name = page.locator("div[class*='content-author '] h5 a")
        self.author_description = page.locator("div[class*='content-author '] div[class*='author-description']")


    def get_author_name(self):
        """Get the author name"""
        return self.author_name.text_content()

    def get_author_href(self):
        """Get the author href attribute"""
        return self.author_name.get_attribute("href")
    
    def get_author_description(self):
        """Get the author description"""
        return self.author_description.text_content()