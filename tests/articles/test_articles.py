from tests.base_test import BaseTest
import time

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

    def test_article_title_and_author(self):
        # Navigate to the home page
        self.home_page.goto()
        # Scroll to the articles
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        self.page.wait_for_load_state("domcontentloaded", timeout=5000)

        # Get the title and author of the article
        title = self.article_page.get_page_title()
        author = self.article_page.get_author()

        assert title == "amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus"
        assert author == "Mark Jecno"

    def test_empty_comment_form(self):
        # Navigate to the home page
        self.home_page.goto()
        # Scroll to the articles
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # check that your name has no invalid class
        class_name = self.article_page.comment_form.get_your_name_class()
        assert "is-invalid" not in class_name

        # Check that email has no invalid class
        email_class_name = self.article_page.comment_form.get_email_input_class()
        assert "is-invalid" not in email_class_name

        # Check that comment has no invalid class
        comment_class_name = self.article_page.comment_form.get_comment_input_class()
        assert "is-invalid" not in comment_class_name

        # Post empty comment
        self.article_page.comment_form.post_comment()
        self.page.wait_for_load_state("networkidle", timeout=5000)


        # Check that your name has invalid class
        class_name = self.article_page.comment_form.get_your_name_class()
        assert "is-invalid" in class_name

        # Check email has no invalid class
        email_class_name = self.article_page.comment_form.get_email_input_class()
        assert "is-invalid" not in email_class_name

        # Check comment has invalid class
        comment_class_name = self.article_page.comment_form.get_comment_input_class()
        assert "is-invalid" in comment_class_name
