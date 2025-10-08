from playwright.sync_api import expect
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

        # Get author name of the first article
        author_name_first_article = self.home_page.articles.get_article_author(index=0)

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        self.page.wait_for_load_state("networkidle", timeout=30000)

        # Get the title and author of the article
        title = self.article_page.get_page_title()
        author_name_article_page = self.article_page.get_author()
        author_href_article_page = self.article_page.get_author_href()

        author_name_on_author_content_component = self.article_page.author_content.get_author_name()
        author_href_on_author_content_component = self.article_page.author_content.get_author_href()

        # Verify that the author href are the same
        assert author_href_article_page == author_href_on_author_content_component

        assert title == "amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus"
        assert author_name_article_page == author_name_first_article
        assert author_name_article_page == author_name_on_author_content_component
        assert author_name_article_page == "Mark Jecno"


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

        # Check your name border color is gray
        your_name_border_color = self.article_page.comment_form.get_your_name_border_color()
        assert your_name_border_color == "rgb(206, 212, 218)"

        # Check that email has no invalid class
        email_class_name = self.article_page.comment_form.get_email_input_class()
        assert "is-invalid" not in email_class_name

        # Check that comment has no invalid class
        comment_class_name = self.article_page.comment_form.get_comment_input_class()
        assert "is-invalid" not in comment_class_name

        # Check that comment border color is gray
        comment_border_color = self.article_page.comment_form.get_comment_border_color()
        assert comment_border_color == "rgb(206, 212, 218)"

        # Post empty comment
        self.article_page.comment_form.post_comment()

        # Check that your name has invalid class
        expect(self.article_page.comment_form.your_name_input).to_have_class("form-control form-control-lg is-invalid")
        
        # Check your name border color change to red
        expect(self.article_page.comment_form.your_name_input).to_have_css("border-color", "rgb(220, 53, 69)")

        # Check email has no invalid class
        email_class_name = self.article_page.comment_form.get_email_input_class()
        assert "is-invalid" not in email_class_name

        # Check comment has invalid class
        expect(self.article_page.comment_form.comment_input).to_have_class("form-control form-control-lg is-invalid")

        # Check that comment border color change to red
        expect(self.article_page.comment_form.comment_input).to_have_css("border-color", "rgb(220, 53, 69)")

    def test_submitted_comment_pending_approval(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        self.page.wait_for_load_state("domcontentloaded", timeout=5000)

        # Fill the comment form and submit it
        self.article_page.comment_form.submit_comment(
            name="John Doe",
            email="john.doe@example.com",
            comment="This is a valid test comment"
        )

        # Verify alert message
        alert_messages = self.article_page.comment_form.alert.get_alert_messages()
        alert_message = alert_messages[0]
        assert "Thank you for your comment. It has been submitted to the webmaster for approval." in alert_message

    def test_default_amount_of_visible_comments(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        # self.article_page.wait_for_page_load(state="domcontentloaded")
        self.article_page.wait_for_page_load(state="networkidle")


        # Check that the amount of visible comments is 5
        assert self.article_page.get_amount_of_visible_comments() == 5

    def test_view_comments_button(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # Check that the amount of visible comments is 5
        expect(self.article_page.comments).to_have_count(5, timeout=10000)

        # Click on the view comments button
        self.article_page.click_on_view_comments_button()

        # Check that the amount of visible comments is 10
        expect(self.article_page.comments).to_have_count(10, timeout=10000)

    def test_view_comments_button_multiple_times(self):
        # Navigate to the home page
        self.home_page.goto()

        # scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # Check that the amount of visible comments is 5
        # Playwright automatically waits, but we need a longer timeout for high concurrency
        expect(self.article_page.comments).to_have_count(5, timeout=30000)

        # Click on the view comments button
        self.article_page.click_on_view_comments_button()

        # Check that the amount of visible comments is 10
        expect(self.article_page.comments).to_have_count(10)

        # Click on the view comments button
        self.article_page.click_on_view_comments_button()

        # Check that the amount of visible comments is 15
        expect(self.article_page.comments).to_have_count(15)

        # Click on the view comments button
        self.article_page.click_on_view_comments_button()

        # Check that the amount of visible comments is 20
        expect(self.article_page.comments).to_have_count(20)

    def test_the_amount_of_related_products(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # Check that the amount of related products is 8
        expect(self.article_page.related_products.related_products).to_have_count(8, timeout=10000)

    def test_add_product_to_wishlist_from_related_products_on_article_page(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # Wait for page to load completely
        self.page.wait_for_load_state("networkidle", timeout=30000)
        
        # Wait for related products section to be visible
        expect(self.article_page.related_products.related_products).to_have_count(8, timeout=30000)

        # Get product name
        product_name = self.article_page.related_products.get_related_product_name(index=0)
        
        # Add product to wishlist from related products
        self.article_page.related_products.add_product_to_wishlist(index=0)

        # Wait for notification to appear
        self.page.wait_for_timeout(1000)
        
        # Verify notification message
        notification_message = self.article_page.notification.get_message_text()
        assert "login" in notification_message
        assert product_name in notification_message
        assert f"You must login or create an account to save {product_name} to your wish list!" in notification_message
        
    def test_add_product_to_cart_from_related_products_on_article_page(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()
        
        # Wait for page to load completely
        self.page.wait_for_load_state("networkidle", timeout=30000)
        
        # Wait for related products section to be visible
        expect(self.article_page.related_products.related_products).to_have_count(8, timeout=30000)
        
        # Get product name
        product_name = self.article_page.related_products.get_related_product_name(index=0)

        # Add product to cart from related products
        self.article_page.related_products.add_product_to_cart(index=0)
        
        # Verify notification message
        notification_message = self.article_page.notification.get_message_text()
        assert "Success:" in notification_message
        assert product_name in notification_message
        assert f"You have added {product_name} to your shopping cart!" in notification_message

    def test_quick_view_product_from_related_products_on_article_page(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()
        
        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # Wait for page to load completely
        self.page.wait_for_load_state("networkidle", timeout=30000)
        
        # Wait for related products section to be visible
        expect(self.article_page.related_products.related_products).to_have_count(8, timeout=30000)

        # Get product name
        product_name = self.article_page.related_products.get_related_product_name(index=0)

        # Open quick view from related products
        self.article_page.related_products.open_quick_view(index=0)

        # Verify quick view modal is open
        expect(self.page.locator(self.article_page.quick_view_modal.container)).to_be_visible(timeout=10000)

        # Verify product name from quick view modal
        product_name_from_quick_view = self.article_page.quick_view_modal.get_product_name()
        assert product_name_from_quick_view == product_name

        # Close quick view modal
        self.article_page.quick_view_modal.close()

        # Verify quick view modal is closed
        expect(self.page.locator(self.article_page.quick_view_modal.container)).to_be_hidden(timeout=10000)
        

    def test_compare_product_from_quick_view_on_article_page(self):
        # Navigate to the home page
        self.home_page.goto()

        # Scroll to the articles section
        self.home_page.articles.scroll_to_articles()

        # Click on the first article
        first_article = self.home_page.articles.article_items.nth(0)
        first_article.click()

        # wait for the page to load
        self.page.wait_for_load_state("networkidle", timeout=30000)

        # Get product name
        product_name = self.article_page.related_products.get_related_product_name(index=0)

        # Open quick view from related products
        self.article_page.related_products.open_quick_view(index=0)

        # Verify quick view modal is open
        expect(self.page.locator(self.article_page.quick_view_modal.container)).to_be_visible(timeout=10000)
        
        # click on the compare button
        self.article_page.quick_view_modal.click_on_compare_button()

        # Verify notification message
        notification_message = self.article_page.notification.get_message_text()
        assert "Success:" in notification_message
        assert product_name in notification_message
        assert f"You have added {product_name} to your product comparison!" in notification_message
