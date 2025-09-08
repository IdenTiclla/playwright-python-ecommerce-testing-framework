from tests.base_test import BaseTest
from utils.data_generator import generate_random_first_name, generate_random_last_name, generate_random_email, generate_random_phone_number, generate_random_password
import time
from playwright.sync_api import expect

class TestProduct(BaseTest):
    def test_first_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        assert self.product_page.get_product_availability() == "Out Of Stock"
    
    def test_second_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.slides.nth(1).click()
        assert self.product_page.get_product_availability() == "Out Of Stock"
    
    def test_third_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.slides.nth(2).click()
        assert self.product_page.get_product_availability() == "In Stock"

    def test_default_quantity_on_product_page(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        assert self.product_page.get_product_quantity() == 1

    def test_top_product_availability(self):
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(0).click()
        url = self.product_page.page.url
        assert url == "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=107"
        assert self.product_page.get_product_name() == "iMac"
        assert self.product_page.get_product_price() == "$170.00"
        assert self.product_page.get_product_availability() == "Out Of Stock"

    def test_increase_quantity_on_product_page(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()
        
        # Get the initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()

        # Increase the quantity of the product by 9
        for i in range(9):
            self.product_page.increase_product_quantity()
        
        # Get the final quantity of the product
        final_quantity = self.product_page.get_product_quantity()
        
        # Assert that the final quantity is the initial quantity plus 9
        assert final_quantity == initial_quantity + 9

    def test_decrease_limit_on_product_page(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Get initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()

        # Decrease the quantity of the product by 9
        for i in range(9):
            self.product_page.decrease_product_quantity()

        # Get final quantity of the product
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity
        assert final_quantity == initial_quantity

    def test_increase_and_decrease_quantity_on_product_page(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Get initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()
        
        # Increase the product's quantity by 9
        for i in range(9):
            self.product_page.increase_product_quantity()

        # Get final product's quantity
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity plus 9
        assert final_quantity == initial_quantity + 9
        
        # Decrease the product's quantity by 9
        for i in range(9):
            self.product_page.decrease_product_quantity()

        # Get final product's quantity
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity
        assert final_quantity == initial_quantity

    def test_add_product_to_cart_from_product_page(self):
        # Navigate to the home page and click on the third product in the carousel
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Get cart count and assert it is 0
        cart_count = self.product_page.header_actions.get_cart_count()
        assert cart_count == "0", f"Cart count should be 0, got: {cart_count}"

        # Add the product to the cart
        self.product_page.add_product_to_cart(quantity=1)

        # Verify notification message

        product_name = self.product_page.get_product_name()

        notification_message = self.product_page.notification.get_message_text()
        print()
        print("notification_message: ", notification_message)
        assert "Success:" in notification_message
        assert product_name in notification_message

        # Close notification
        self.product_page.notification.close()

        # Get cart count
        cart_count = self.product_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1, got: {cart_count}"

    def test_add_five_products_to_cart_from_product_page(self):
        # Navigate to the home page and click on the third product in the carousel
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Get cart count and assert it is 0
        cart_count = self.product_page.header_actions.get_cart_count()
        assert cart_count == "0", f"Cart count should be 0, got: {cart_count}"

        # Add the product to the cart
        self.product_page.add_product_to_cart(quantity=5)

        # Verify notification message

        product_name = self.product_page.get_product_name()

        notification_message = self.product_page.notification.get_message_text()
        
        assert "Success:" in notification_message
        assert product_name in notification_message

        # Close notification
        self.product_page.notification.close()

        # Get cart count
        cart_count = self.product_page.header_actions.get_cart_count()
        assert cart_count == "5", f"Cart count should be 5, got: {cart_count}"

    def test_add_review_without_rating(self):
        # Navigate to the home page and click on third product of top products
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Add review without rating
        self.product_page.review_form.submit_review(rating=0, name="John Doe", review="This is a review")
        
        # Verify error message
        error_message = self.product_page.review_form.get_error_message()
        expected_error_message = "Warning: Please select a review rating!"
        assert error_message == expected_error_message

    def test_add_empty_name_and_review(self):
        # Navigate to the home page and click on third product of top products
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Add empty review
        self.product_page.review_form.submit_review(rating=1, name="", review="")
        
        # Verify error message
        error_message = self.product_page.review_form.get_error_message()
        assert error_message == "Warning: Review Text must be between 25 and 1000 characters!"

    def test_add_review_with_empty_name(self):
        # Navigate to the home page and click on third product of top products
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Add empty review
        self.product_page.review_form.submit_review(rating=1, name="", review="This is a review with a proper length")

        # Verify error message
        error_message = self.product_page.review_form.get_error_message()
        assert error_message == "Warning: Review Name must be between 3 and 25 characters!"

    def test_add_product_to_wishlist_from_product_page_without_login(self):
        # Navigate to the home page and click on third product of top products
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Get product name
        product_name = self.product_page.get_product_name()

        # Add product to wishlist
        self.product_page.add_product_to_wishlist()

        # Verify notification message
        notification_message = self.product_page.notification.get_message_text()
        assert "login" in notification_message
        assert "You must login or create an account to save iMac to your wish list!" in notification_message
        
        # Verify product name in notification message
        assert product_name in notification_message

    def test_add_product_to_wishlist_from_product_page_with_logged_user(self):
        # Create a new user
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        password = generate_random_password()
        self.register_page.register(
            firstname=generate_random_first_name(),
            lastname=generate_random_last_name(),
            email=generate_random_email(),
            telephone=generate_random_phone_number(),
            password=password,
            password_confirm=password,
            subscribe_newsletter=True,
            accept_terms=True
        )
        
        # Navigate to product page
        self.success_page.wait_for_page_load()
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(3).click()
        self.product_page.wait_for_page_load()

        # Get product name
        product_name = self.product_page.get_product_name()

        # Add product to wishlist
        self.product_page.add_product_to_wishlist()

        # Verify notification message
        notification_message = self.product_page.notification.get_message_text()
        assert f"Success: You have added {product_name} to your wish list!" == notification_message

        # Verify product name in notification message
        assert product_name in notification_message

        # Close notification
        self.product_page.notification.close()

        # Verify product name in wishlist
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        assert product_name in self.wishlist_page.get_product_details(0)["product_name"]

        # Verify product quantity in wishlist
        assert self.wishlist_page.get_wishlist_items_count() == 1

    def test_first_image_on_carousel_has_related_products(self):
        # Navigate to the home page and click on the third product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Verify related products
        assert self.product_page.related_products.get_related_products_count() > 0
        assert self.product_page.related_products.get_related_products_count() == 8

    def test_second_image_on_carousel_does_not_have_related_products(self):
        # Navigate to the home page and click on the third product in the carousel
        self.home_page.goto()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.slides.nth(1).click()
        self.product_page.wait_for_page_load()

        # Verify related products
        assert self.product_page.related_products.get_related_products_count() == 0

    def test_add_product_to_wishlist_from_related_products(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Get product name
        product_name = self.product_page.related_products.get_related_product_name(index=0)
        
        # Add product to wishlist
        self.product_page.related_products.add_product_to_wishlist(index=0)

        # Verify notification message
        notification_message = self.product_page.notification.get_message_text()
        assert "login" in notification_message
        assert product_name in notification_message
        assert f"You must login or create an account to save {product_name} to your wish list!" in notification_message

    def test_open_and_close_quick_view_from_related_products(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Open quick view from related products
        self.product_page.related_products.open_quick_view(index=0)

        # self.page.wait_for_load_state("networkidle", timeout=10000)

        # Verify quick view modal is open
        expect(self.page.locator(self.product_page.quick_view_modal.container)).to_be_visible(timeout=10000)

        # Close quick view modal
        self.product_page.quick_view_modal.close()

        # self.page.wait_for_load_state("networkidle", timeout=10000)

        # Verify quick view modal is closed
        # assert not self.product_page.quick_view_modal.is_visible()
        expect(self.page.locator(self.product_page.quick_view_modal.container)).to_be_hidden(timeout=10000)