from playwright.sync_api import Page
from components.base_component import BaseComponent

class Articles(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.container = self.page.locator("//*[contains(text(), 'From The Blog')]/parent::div//following-sibling::div[contains(@class, 'article_listing')]")
        self.article_items = self.page.locator("//div[contains(@class, 'mz_article_listing')]//div[contains(@class, 'article-thumb')]")
        self.article_titles = "h4.title"
        self.article_links = "div.image a"
        self.article_authors= "div.metadata span.author a"
        self.article_comments = "div.metadata span.comment"
        self.article_views = "div.metadata span.viewed"

        self.next_button = page.locator("div[id*='article'] a.swiper-button-next")
        self.prev_button = page.locator("div[id*='article'] a.swiper-button-prev")


    def click_next_button(self):
        self.next_button.click(force=True)
        self.page.wait_for_timeout(200)

    def click_prev_button(self):
        self.prev_button.click()

    def get_article_title(self, index=0):
        return self.article_items.nth(index).locator(self.article_titles).text_content()
    
    def get_article_author(self, index=0):
        return self.article_items.nth(index).locator(self.article_authors).text_content()

    def scroll_to_articles(self):
        self.container.scroll_into_view_if_needed()
    
    
