from tests.base_test import BaseTest


class TestArticles(BaseTest):
    def test_defualt_articles_count(self):
        """Test that the default articles count is 10."""
        self.home_page.goto()
        self.home_page.articles.scroll_to_articles()
        assert self.home_page.articles.article_items.count() == 10

    def test_url_after_click_on_first_article(self):
        self.home_page.goto()
        self.home_page.articles.scroll_to_articles()

        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        self.page.wait_for_load_state("domcontentloaded", timeout=5000)

        assert self.page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/blog/article&article_id=37"