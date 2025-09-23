from playwright.sync_api import Page
from pages.base_page import BasePage
from components.comment_form import CommentForm

class ArticlePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Components
        self.comment_form = CommentForm(page)

        # Locators
        self.page_title = self.page.locator("h1.h1")
        self.author = self.page.locator("a.author")
        self.views_amount = self.page.locator("span.extra-viewed")
        self.comments_amount = self.page.locator("span.extra-comments")
        self.comments = self.page.locator("div#comment ul li")
        self.view_comments_button = self.page.locator("ul a.view-replies")

    def get_page_title(self):
        return self.page_title.text_content().strip()

    def get_author(self):
        return self.author.text_content().strip()

    def get_views_amount(self):
        """Get the amount of views"""
        return self.views.text_content().strip()
    
    def get_total_amount_of_comments(self):
        """Get the amount of comments"""
        return self.comments.text_content().strip().replace("comments", "")

    def get_amount_of_visible_comments(self):
        return self.comments.count()

    def click_on_view_comments_button(self):
        self.view_comments_button.click()