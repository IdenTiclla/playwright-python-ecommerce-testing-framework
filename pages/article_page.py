from playwright.sync_api import Page
from pages.base_page import BasePage
from components.comment_form import CommentForm
from components.related_products import RelatedProducts
from components.notification import Notification
from components.quick_view_modal import QuickViewModal
from components.author_content import AuthorContent
from components.related_articles import RelatedArticles

class ArticlePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Components
        self.comment_form = CommentForm(page)
        self.related_products = RelatedProducts(page)
        self.notification = Notification(page)
        self.quick_view_modal = QuickViewModal(page)
        self.author_content = AuthorContent(page)
        self.related_articles = RelatedArticles(page)

        # Locators
        self.page_title = self.page.locator("h1.h1")
        self.author = self.page.locator("a.author")
        self.views_amount = self.page.locator("span.extra-viewed")
        self.comments_amount = self.page.locator("span.extra-comments")
        self.comments = self.page.locator("div#comment ul li")
        self.view_comments_button = self.page.locator("ul a.view-replies")
        self.cancel_reply_button = self.page.locator("//a[contains(text(), 'Cancel reply')]")

    def click_on_comments_reply_button(self, index: int = 0):
        """Click on the reply button of a comment by index (0-based)"""
        self.comments.nth(index).locator("a.reply").click()

    def get_page_title(self):
        return self.page_title.text_content().strip()

    def get_author(self):
        return self.author.text_content().strip()

    def get_author_href(self):
        """Get the author href attribute"""
        return self.author.get_attribute("href")

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