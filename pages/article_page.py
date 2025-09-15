from playwright.sync_api import Page
from pages.base_page import BasePage


class ArticlePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.page_title = self.page.locator("h1.h1")
        self.author = self.page.locator("a.author")
        self.views = self.page.locator("span.extra-viewed")
        self.comments = self.page.locator("span.extra-comments")

    def get_page_title(self):
        return self.page_title.text_content().strip()

    def get_author(self):
        return self.author.text_content().strip()

    def get_views_amount(self):
        """Get the amount of views"""
        return self.views.text_content().strip()
    
    def get_comments_amount(self):
        """Get the amount of comments"""
        return self.comments.text_content().strip().replace("comments", "")
