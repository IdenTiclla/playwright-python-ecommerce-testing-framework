from playwright.sync_api import Page
from components.base_component import BaseComponent

class RelatedArticles(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.related_articles = page.locator("div[id*='mz-article-tab'] div.swiper-slide")
        self.article_author = "span.author"
        self.article_date = "span.timestamp"
        self.article_amount_comments = "span.comment"
        self.article_amount_views = "span.viewed"
        self.article_title = "h4.title"

    def get_related_articles_count(self):
        """Get the number of related articles"""
        return self.related_articles.count()


    def get_article_timestamp(self, index=0):
        """Get the timestamp of a related article"""
        return self.related_articles.nth(index).locator(self.article_date).text_content().strip()
    
    def get_article_author(self, index=0):
        """Get the author of a related article"""
        return self.related_articles.nth(index).locator(self.article_author).text_content().strip()

    def get_article_amount_comments(self, index=0):
        """Get the amount of comments of a related article"""
        return self.related_articles.nth(index).locator(self.article_amount_comments).text_content().strip()
    
    def get_article_amount_views(self, index=0):
        """Get the amount of views of a related article"""
        return self.related_articles.nth(index).locator(self.article_amount_views).text_content().strip()
    
    def get_article_title(self, index=0):
        """Get the title of a related article"""
        return self.related_articles.nth(index).locator(self.article_title).text_content().strip()