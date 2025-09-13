from tests.base_test import BaseTest


class TestArticles(BaseTest):
    def test_defualt_articles_count(self):
        """Test that the default articles count is 10."""
        self.home_page.goto()
        self.home_page.articles.scroll_to_articles()
        assert self.home_page.articles.article_items.count() == 10
