import os
import pytest
from playwright.sync_api import expect
from pages.wishlist_page import WishlistPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
import random

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

class TestWishlistPage:
    """Test suite for Wishlist Page functionality"""

    @pytest.fixture
    def wishlist_page(self, page) -> WishlistPage:
        return WishlistPage(page)

    @pytest.fixture
    def home_page(self, page) -> HomePage:
        return HomePage(page)

    @pytest.fixture
    def login_page(self, page) -> LoginPage:
        return LoginPage(page)

    @pytest.fixture
    def register_page(self, page) -> RegisterPage:
        return RegisterPage(page)

    def test_wishlist_page_navigation_without_logged_user(self, wishlist_page):
        """Test direct navigation to wishlist page"""
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Verify page title
        page_title = wishlist_page.page.title()
        assert "Account Login" in page_title, f"Expected 'Account Login' in page title, got: {page_title}"
        
        # Verify URL
        current_url = wishlist_page.page.url
        assert "account/login" in current_url, f"Expected 'account/login' in URL, got: {current_url}"

    def test_wishlist_page_with_logged_user_and_no_products(self, wishlist_page, home_page, login_page, page):
        """Test wishlist page with logged user and no products"""
        home_page.goto()
        home_page.navbar_horizontal.click_my_account_option("Login")
        email = os.getenv("VALID_EMAIL")
        password = os.getenv("VALID_PASSWORD")
        login_page.login(email, password)
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Verify page title
        page_title = wishlist_page.page.title()
        assert "My Wish List" in page_title, f"Expected 'My Wish List' in page title, got: {page_title}"
        
        no_results_message = page.locator(wishlist_page.no_results_message).text_content()
        assert "No results!" in no_results_message, f"Expected 'No results!' in no results message, got: {no_results_message}"

    def test_wishlist_page_elements_visibility(self, wishlist_page, page, home_page, login_page, register_page):
        """Test that all main page elements are visible"""
        home_page.goto()
        home_page.navbar_horizontal.click_my_account_option("Register")
        random_firstname = f"John{random.randint(1, 1000000)}"
        random_lastname = f"Doe{random.randint(1, 1000000)}"
        random_email = f"john.doe{random.randint(1, 1000000)}@example.com"
        random_telephone = f"1234567890{random.randint(1, 1000000)}"
        random_password = "TestPassword123!"
        register_page.register(firstname=random_firstname, lastname=random_lastname, email=random_email, telephone=random_telephone, password=random_password, subscribe_newsletter=False)
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Check main elements
        assert wishlist_page.is_wishlist_table_visible(), "Wishlist table should be visible"
        
        # Check breadcrumb
        breadcrumb_text = wishlist_page.get_breadcrumb_text()
        assert "My Wish List" in breadcrumb_text, f"Expected 'My Wish List' in breadcrumb, got: {breadcrumb_text}"

    def test_wishlist_table_headers(self, wishlist_page, home_page, login_page, register_page, page):
        """Test that wishlist table has correct headers"""
        home_page.goto()
        home_page.navbar_horizontal.click_my_account_option("Register")
        random_firstname = f"John{random.randint(1, 1000000)}"
        random_lastname = f"Doe{random.randint(1, 1000000)}"
        random_email = f"john.doe{random.randint(1, 1000000)}@example.com"
        random_telephone = f"1234567890{random.randint(1, 1000000)}"
        random_password = "TestPassword123!"
        register_page.register(firstname=random_firstname, lastname=random_lastname, email=random_email, telephone=random_telephone, password=random_password, subscribe_newsletter=False)
        
        # add a product to wishlist
        home_page.goto()
        home_page.top_products.add_product_to_wishlist(index=0)
        page.wait_for_timeout(2000)
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        headers = wishlist_page.get_table_headers()
        expected_headers = ["Image", "Product Name", "Model", "Stock", "Unit Price", "Action"]
        
        for expected_header in expected_headers:
            assert expected_header in headers, f"Expected header '{expected_header}' not found in {headers}"

    def test_wishlist_with_logged_in_user_and_products(self, home_page, login_page, wishlist_page, page):
        """Test wishlist functionality with a logged-in user who has products in wishlist"""
        # First, register and login a user
        home_page.goto()
        page.wait_for_timeout(1000)
        
        # Navigate to login page
        home_page.click_on_login()
        page.wait_for_timeout(1000)
        
        # Login with test credentials (assuming these exist or we create them)
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        page.wait_for_timeout(2000)
        
        # Go to home page and add product to wishlist
        home_page.goto()
        page.wait_for_timeout(1000)
        
        # Add product to wishlist from top products
        home_page.top_products.scroll_to_top_products()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)
        
        # Add first product to wishlist
        home_page.top_products.add_product_to_wishlist(index=0)
        page.wait_for_timeout(2000)
        
        # Navigate to wishlist page
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Verify product is in wishlist
        items_count = wishlist_page.get_wishlist_items_count()
        assert items_count > 0, "Wishlist should contain at least one item"
        
        # Get product details
        product_details = wishlist_page.get_product_details(0)
        assert product_details["product_name"], "Product name should not be empty"
        assert product_details["price"], "Product price should not be empty"
        assert product_details["model"], "Product model should not be empty"

    def test_wishlist_product_details_display(self, wishlist_page, home_page, login_page, page):
        """Test that product details are correctly displayed in wishlist"""
        # Setup: Login and add product to wishlist
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        # Navigate to wishlist
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Skip if no items in wishlist
        if wishlist_page.get_wishlist_items_count() == 0:
            pytest.skip("No items in wishlist to test")
        
        # Test product details
        product_details = wishlist_page.get_product_details(0)
        
        # Verify all required fields are present
        assert product_details["product_name"], "Product name should be present"
        assert product_details["model"], "Product model should be present"
        assert product_details["stock_status"], "Stock status should be present"
        assert product_details["price"], "Product price should be present"
        assert product_details["image_src"], "Product image should be present"
        
        # Verify price format
        price = product_details["price"]
        assert "$" in price, f"Price should contain '$' symbol, got: {price}"

    def test_wishlist_product_navigation(self, wishlist_page, home_page, login_page, page):
        """Test navigation from wishlist to product page"""
        # Setup: Login and ensure product in wishlist
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        if wishlist_page.get_wishlist_items_count() == 0:
            pytest.skip("No items in wishlist to test navigation")
        
        # Get product name before navigation
        product_details = wishlist_page.get_product_details(0)
        product_name = product_details["product_name"]
        
        # Click on product name
        wishlist_page.click_product_name(0)
        page.wait_for_timeout(2000)
        
        # Verify navigation to product page
        current_url = page.url
        assert "product/product" in current_url, f"Should navigate to product page, current URL: {current_url}"

    def test_remove_product_from_wishlist(self, wishlist_page, home_page, login_page, page):
        """Test removing a product from wishlist"""
        # Setup: Login and ensure product in wishlist
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        # Add product to wishlist first
        home_page.goto()
        home_page.top_products.scroll_to_top_products()
        page.wait_for_load_state("domcontentloaded")
        home_page.top_products.add_product_to_wishlist(index=0)
        page.wait_for_timeout(2000)
        
        # Go to wishlist
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        initial_count = wishlist_page.get_wishlist_items_count()
        if initial_count == 0:
            pytest.skip("No items in wishlist to remove")
        
        # Remove first product
        wishlist_page.remove_from_wishlist(0)
        page.wait_for_timeout(2000)
        
        # Verify product was removed
        new_count = wishlist_page.get_wishlist_items_count()
        assert new_count == initial_count - 1, f"Expected {initial_count - 1} items, got {new_count}"

    def test_wishlist_sidebar_navigation(self, wishlist_page, home_page, login_page, page):
        """Test sidebar navigation links"""
        # Setup: Login first
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Test My Account navigation
        wishlist_page.click_my_account()
        page.wait_for_timeout(1000)
        assert "account/account" in page.url, "Should navigate to My Account page"
        
        # Go back to wishlist
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Test Edit Account navigation
        wishlist_page.click_edit_account()
        page.wait_for_timeout(1000)
        assert "account/edit" in page.url, "Should navigate to Edit Account page"

    def test_continue_button_functionality(self, wishlist_page, home_page, login_page, page):
        """Test the Continue button functionality"""
        # Setup: Login first
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Click continue button
        wishlist_page.click_continue()
        page.wait_for_timeout(1000)
        
        # Verify navigation to account page
        assert "account/account" in page.url, "Continue button should navigate to My Account page"

    def test_wishlist_stock_status_display(self, wishlist_page, home_page, login_page, page):
        """Test that stock status is correctly displayed"""
        # Setup: Login and ensure product in wishlist
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        if wishlist_page.get_wishlist_items_count() == 0:
            pytest.skip("No items in wishlist to test stock status")
        
        # Check stock status
        stock_status = wishlist_page.get_stock_status(0)
        assert stock_status in ["In Stock", "Out Of Stock", "Pre-Order"], f"Unexpected stock status: {stock_status}"

    def test_wishlist_empty_state(self, wishlist_page, home_page, login_page, page):
        """Test wishlist when it's empty"""
        # Setup: Login first
        home_page.goto()
        home_page.click_on_login()
        login_page.login("john.doe.test@example.com", "TestPassword123!")
        
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Remove all items if any exist
        while wishlist_page.get_wishlist_items_count() > 0:
            wishlist_page.remove_from_wishlist(0)
            page.wait_for_timeout(1000)
            wishlist_page.page.reload()
            wishlist_page.wait_for_page_load()
        
        # Verify empty state
        items_count = wishlist_page.get_wishlist_items_count()
        assert items_count == 0, "Wishlist should be empty"

    def test_wishlist_page_responsive_elements(self, wishlist_page, page):
        """Test that wishlist page elements are responsive"""
        wishlist_page.goto()
        wishlist_page.wait_for_page_load()
        
        # Test different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 768, "height": 1024},   # Tablet
            {"width": 375, "height": 667},    # Mobile
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            page.wait_for_timeout(500)
            
            # Verify main elements are still visible
            assert wishlist_page.is_wishlist_table_visible(), f"Table should be visible at {viewport['width']}x{viewport['height']}"
            
            page_title = wishlist_page.get_page_title()
            assert "My Wish List" in page_title, f"Page title should be visible at {viewport['width']}x{viewport['height']}" 