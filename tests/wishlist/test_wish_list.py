from playwright.sync_api import expect
from tests.base_test import BaseTest
import random
import pytest

class TestWishList(BaseTest):
    def test_add_to_wishlist_from_top_products_without_login(self):
        # home_page.goto()
        self.home_page.goto()
        # self.page.wait_for_timeout(1000)

        self.home_page.top_products.scroll_to_top_products()
        # expect(home_page.top_products.section).to_be_visible(timeout=10000)

        # Esperar a que el dom este cargado
        # self.page.wait_for_load_state("domcontentloaded")

        # verificar que la seccion de productos top esta visible
        # assert self.page.locator(self.home_page.top_products.section).is_visible(timeout=10000), "Top products section should be visible"
        # self.page.wait_for_timeout(1000)

        self.home_page.top_products.add_product_to_wishlist(index=0)
        # self.page.wait_for_timeout(1000)

        # verificar que se muestra la notificacion
        expect(self.home_page.notification.container).to_be_visible()

        # verificar el texto de la notificacion
        notification_title = self.home_page.notification.get_title_text()
        notification_message = self.home_page.notification.get_message_text()

        # verificar el texto del boton de login
        login_button_text = self.home_page.notification.get_login_button_text()
        # verificar el texto del boton de register
        register_button_text = self.home_page.notification.get_register_button_text()

        # verificar el titulo de la notificacion
        assert "Login" in notification_title, "Notification title should be 'Login'"
        assert "You must login or create an account to save iMac to your wish list!" in notification_message, "Notification message should be 'You must be login or create an account to save iMac to your wishlist.'"
        assert "Login" in login_button_text, "Login button text should be 'Login'"
        assert "Register" in register_button_text, "Register button text should be 'Register'"
        

        # cerrar la notificacion
        self.home_page.notification.close()

        # verificar que la notificacion se cierra
        expect(self.home_page.notification.container).to_be_hidden()

    
    def test_add_to_wishlist_from_quick_view_without_login(self):
        self.home_page.goto()

        self.home_page.top_products.scroll_to_top_products()
        

        self.home_page.top_products.show_quick_view(index=0)

        self.home_page.quick_view_modal.add_to_wishlist()

        # expect(self.page.locator(self.home_page.notification.container)).to_be_visible(timeout=10000)

        expect(self.home_page.notification.container).to_be_visible()

        notification_title = self.home_page.notification.get_title_text()
        notification_message = self.home_page.notification.get_message_text()
        notification_login_button_text = self.home_page.notification.get_login_button_text()
        notification_register_button_text = self.home_page.notification.get_register_button_text()

        assert "Login" in notification_title, "Notification title should be 'Login'"
        assert "You must login or create an account to save iMac to your wish list!" in notification_message, "Notification message should be 'You must be login or create an account to save iMac to your wishlist.'"
        assert "Login" in notification_login_button_text, "Login button text should be 'Login'"
        assert "Register" in notification_register_button_text, "Register button text should be 'Register'"
        
        # cerrar la notificacion
        self.home_page.notification.close()

        # verificar que la notificacion se cierra
        # expect(self.page.locator(self.home_page.notification.container)).not_to_be_visible(timeout=10000)
        expect(self.home_page.notification.container).not_to_be_visible()

    def test_wishlist_page_navigation_without_logged_user(self):
        """Test direct navigation to wishlist page"""
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Verify page title
        page_title = self.wishlist_page.page.title()
        assert "Account Login" in page_title, f"Expected 'Account Login' in page title, got: {page_title}"
        
        # Verify URL
        current_url = self.wishlist_page.page.url
        assert "account/login" in current_url, f"Expected 'account/login' in URL, got: {current_url}"

    def test_wishlist_page_with_new_user_account_and_no_products(self):
        """Test wishlist page with new user account and no products"""
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        random_firstname = f"John{random.randint(1, 1000000)}"
        random_lastname = f"Doe{random.randint(1, 1000000)}"
        random_email = f"john.doe{random.randint(1, 1000000)}@example.com"
        random_telephone = f"1234567890{random.randint(1, 1000000)}"
        random_password = "TestPassword123!"
        self.register_page.register(
            firstname=random_firstname,
            lastname=random_lastname,
            email=random_email,
            telephone=random_telephone,
            password=random_password,
            password_confirm=random_password,
            subscribe_newsletter=False,
            accept_terms=True
        )

        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Verify page title
        page_title = self.wishlist_page.page.title()
        assert "My Wish List" in page_title, f"Expected 'My Wish List' in page title, got: {page_title}"
        
        no_results_message = self.wishlist_page.get_no_results_message()
        assert "No results!" in no_results_message, f"Expected 'No results!' in no results message, got: {no_results_message}"

    def test_wishlist_page_elements_visibility(self):
        """Test that all main page elements are visible"""
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        random_firstname = f"John{random.randint(1, 1000000)}"
        random_lastname = f"Doe{random.randint(1, 1000000)}"
        random_email = f"john.doe{random.randint(1, 1000000)}@example.com"
        random_telephone = f"1234567890{random.randint(1, 1000000)}"
        random_password = "TestPassword123!"
        self.register_page.register(
            firstname=random_firstname,
            lastname=random_lastname,
            email=random_email,
            telephone=random_telephone,
            password=random_password,
            password_confirm=random_password,
            subscribe_newsletter=False,
            accept_terms=True
        )

        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Check main elements
        assert not self.wishlist_page.is_wishlist_table_visible(), "Wishlist table should be visible"
        
        # Check breadcrumb
        breadcrumb_text = self.wishlist_page.get_breadcrumb_text()
        assert "My Wish List" in breadcrumb_text, f"Expected 'My Wish List' in breadcrumb, got: {breadcrumb_text}"

    def test_wishlist_table_headers(self):
        """Test that wishlist table has correct headers"""
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        random_firstname = f"John{random.randint(1, 1000000)}"
        random_lastname = f"Doe{random.randint(1, 1000000)}"
        random_email = f"john.doe{random.randint(1, 1000000)}@example.com"
        random_telephone = f"1234567890{random.randint(1, 1000000)}"
        random_password = "TestPassword123!"
        self.register_page.register(
            firstname=random_firstname,
            lastname=random_lastname,
            email=random_email,
            telephone=random_telephone,
            password=random_password,
            password_confirm=random_password, subscribe_newsletter=False,
            accept_terms=True
        )

        # add a product to wishlist
        self.home_page.goto()
        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(2000)
        
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        headers = self.wishlist_page.get_table_headers()
        expected_headers = ["Image", "Product Name", "Model", "Stock", "Unit Price", "Action"]
        
        for expected_header in expected_headers:
            assert expected_header in headers, f"Expected header '{expected_header}' not found in {headers}"

    def test_wishlist_with_logged_in_user_and_products(self):
        """Test wishlist functionality with a logged-in user who has products in wishlist"""
        # First, register and login a user
        self.home_page.goto()
        self.page.wait_for_timeout(1000)
        
        # Navigate to login page
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.page.wait_for_timeout(1000)

        self.home_page.navbar_horizontal.click_my_account_option("Login")
        
        # Login with test credentials (assuming these exist or we create them)
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        self.page.wait_for_timeout(2000)
        
        # Go to home page and add product to wishlist
        self.home_page.goto()
        self.page.wait_for_timeout(1000)
        
        # Add product to wishlist from top products
        self.home_page.top_products.scroll_to_top_products()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)
        
        # Add first product to wishlist
        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(2000)
        
        # Navigate to wishlist page
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Verify product is in wishlist
        items_count = self.wishlist_page.get_wishlist_items_count()
        assert items_count > 0, "Wishlist should contain at least one item"
        
        # Get product details
        product_details = self.wishlist_page.get_product_details(0)
        assert product_details["image_src"], "Product image should not be empty"
        assert product_details["product_name"], "Product name should not be empty"
        assert product_details["model"], "Product model should not be empty"
        assert product_details["stock_status"], "Product stock status should not be empty"
        assert product_details["price"], "Product price should not be empty"

        # logs
        print(product_details)
        
        assert product_details["image_src"] == "https://ecommerce-playground.lambdatest.io/image/cache/catalog/maza/demo/mz_poco/megastore-2/product/10-47x47.webp", "Product image should be the same as the one in the wishlist"
        assert product_details["product_name"] == "iMac", "Product name should be the same as the one in the wishlist"
        assert product_details["model"] == "Product 14", "Product model should be the same as the one in the wishlist"
        assert product_details["stock_status"] == "Out Of Stock", "Product stock status should be the same as the one in the wishlist"
        assert product_details["price"] == "$170.00", "Product price should be the same as the one in the wishlist"

        assert "$" in product_details["price"], "Product price should contain $ symbol"

    def test_wishlist_product_navigation(self):
        """Test navigation from wishlist to product page"""
        # Setup: Login and ensure product in wishlist
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        if self.wishlist_page.get_wishlist_items_count() == 0:
            pytest.skip("No items in wishlist to test navigation")
        
        # Get product name before navigation
        product_details = self.wishlist_page.get_product_details(0)
        product_name = product_details["product_name"]
        
        # Click on product name
        self.wishlist_page.click_product_name(0)
        self.page.wait_for_timeout(2000)
        
        # Verify navigation to product page
        current_url = self.page.url
        assert "product/product" in current_url, f"Should navigate to product page, current URL: {current_url}"

    def test_remove_product_from_wishlist(self):
        """Test removing a product from wishlist"""
        # Setup: Login and ensure product in wishlist
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        # Add product to wishlist first
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(2000)
        
        # Go to wishlist
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        initial_count = self.wishlist_page.get_wishlist_items_count()
        if initial_count == 0:
            pytest.skip("No items in wishlist to remove")
        
        # Remove first product
        self.wishlist_page.remove_from_wishlist(0)
        self.page.wait_for_timeout(2000)
    
        # Verify alert is visible
        assert self.wishlist_page.alert_component.is_visible(), "Alert should be visible"
        alert_messages = self.wishlist_page.alert_component.get_alert_messages()
        assert any("Success: You have modified your wish list!" in alert_message for alert_message in alert_messages)
        
        # Verify product was removed
        new_count = self.wishlist_page.get_wishlist_items_count()
        assert new_count == initial_count - 1, f"Expected {initial_count - 1} items, got {new_count}"

    def test_wishlist_sidebar_navigation(self):
        """Test sidebar navigation links"""
        # Setup: Login first
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.wait_for_page_load()
        quantity_of_sidebar_links = self.login_page.sidebar_navigation_component.get_quantity_of_sidebar_links()
        assert quantity_of_sidebar_links == 13, f"Expected 13 sidebar links, got {quantity_of_sidebar_links}"
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        quantity_of_sidebar_links = self.wishlist_page.sidebar_navigation.get_quantity_of_sidebar_links()
        assert quantity_of_sidebar_links == 14, f"Expected 14 sidebar links, got {quantity_of_sidebar_links}"

        # Test My Account navigation
        self.wishlist_page.sidebar_navigation.click_my_account_option()
        self.page.wait_for_timeout(1000)
        assert "account/account" in self.page.url, "Should navigate to My Account page"
        
        # Go back to wishlist
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Test Edit Account navigation
        self.wishlist_page.sidebar_navigation.click_edit_account_option()
        self.page.wait_for_timeout(1000)
        assert "account/edit" in self.page.url, "Should navigate to Edit Account page"

    def test_continue_button_functionality(self):
        """Test the Continue button functionality"""
        # Setup: Login first
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.wait_for_page_load()
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Click continue button
        self.wishlist_page.click_continue()
        self.wishlist_page.wait_for_page_load()
        
        # Verify navigation to account page
        assert "account/account" in self.page.url, "Continue button should navigate to My Account page"
        self.account_page.wait_for_page_load()
        quantity_of_sidebar_links = self.account_page.sidebar_navigation.get_quantity_of_sidebar_links()
        assert quantity_of_sidebar_links == 14, f"Expected 14 sidebar links, got {quantity_of_sidebar_links}"

    def test_wishlist_stock_status_display(self):
        """Test that stock status is correctly displayed"""
        # Setup: Login and ensure product in wishlist
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.wait_for_page_load()
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        if self.wishlist_page.get_wishlist_items_count() == 0:
            pytest.skip("No items in wishlist to test stock status")
        
        # Check stock status
        stock_status = self.wishlist_page.get_stock_status(0)
        assert stock_status in ["In Stock", "Out Of Stock", "Pre-Order"], f"Unexpected stock status: {stock_status}"
        assert stock_status == "Out Of Stock", f"Expected 'Out Of Stock' stock status, got {stock_status}"

    def test_wishlist_empty_state(self):
        """Test wishlist when it's empty"""
        # Setup: Login first
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.wait_for_page_load()
        self.login_page.login("test@qwertest.com", "P@ssw0rd")
        
        # add a product to wishlist
        self.home_page.goto()
        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(2000)

        # add another product to wishlist
        self.home_page.goto()
        self.home_page.top_products.add_product_to_wishlist(index=1)
        self.page.wait_for_timeout(2000)

        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        
        # Verify empty state
        self.wishlist_page.remove_all_from_wishlist()
        items_count = self.wishlist_page.get_wishlist_items_count()
        assert items_count == 0, "Wishlist should be empty"

        # Verify no results message
        no_results_message = self.wishlist_page.get_no_results_message()
        assert "No results!" in no_results_message, f"Expected 'No results!' in no results message, got: {no_results_message}"

    def test_wishlist_page_responsive_elements(self):
        """Test that wishlist page elements are responsive"""
        # login a user
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Login")
        self.login_page.wait_for_page_load()
        self.login_page.login("test@qwertest.com", "P@ssw0rd")

        # add a product to wishlist
        self.home_page.goto()
        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(2000)

        self.wishlist_page.goto()
        self.wishlist_page.wait_for_page_load()
        
        # Test different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 768, "height": 1024},   # Tablet
            {"width": 375, "height": 667},    # Mobile
        ]
        
        for viewport in viewports:
            self.page.set_viewport_size(viewport)    
            self.page.wait_for_timeout(500)
            
            # Verify main elements are still visible
            assert self.wishlist_page.is_wishlist_table_visible(), f"Table should be visible at {viewport['width']}x{viewport['height']}"
            
            page_title = self.wishlist_page.get_page_title()
            assert "My Wish List" in page_title, f"Page title should be visible at {viewport['width']}x{viewport['height']}" 