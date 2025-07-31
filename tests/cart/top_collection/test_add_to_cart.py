import pytest
from playwright.sync_api import expect
from tests.base_test import BaseTest
from utils.data_generator import (
    generate_random_email, 
    generate_random_first_name, 
    generate_random_last_name, 
    generate_random_phone_number, 
    generate_random_password
)

class TestTopCollectionAddToCart(BaseTest):
    """
    Test cases for adding products from Top Collection section to shopping cart.
    Covers all three tabs: POPULAR, LATEST, and BEST SELLER.
    """

    @pytest.fixture(autouse=True)
    def setup_registered_user(self):
        """
        Setup a registered user for each test to ensure clean cart state.
        This fixture runs before each test method.
        """
        # Navigate to home page and register a new user
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        
        # Generate unique user data for each test
        generated_password = generate_random_password()
        self.register_page.register(
            firstname=generate_random_first_name(),
            lastname=generate_random_last_name(),
            email=generate_random_email(),
            telephone=generate_random_phone_number(),
            password=generated_password,
            password_confirm=generated_password,
            subscribe_newsletter=True,
            accept_terms=True
        )
        
        # Wait for registration success and return to home page
        self.success_page.wait_for_page_load()
        self.home_page.goto()
        self.home_page.wait_for_page_load()
        
        # Verify initial cart state is empty
        initial_cart_count = self.home_page.header_actions.get_cart_count()
        assert initial_cart_count == "0", f"Cart should be empty initially, but shows {initial_cart_count}"

    def test_add_product_to_cart_from_popular_tab(self):
        """
        Test adding a product to cart from the POPULAR tab.
        
        Steps:
        1. Navigate to Top Collection section
        2. Switch to POPULAR tab
        3. Get product information before adding
        4. Add first product to cart
        5. Verify success notification appears
        6. Verify cart counter updates
        7. Verify cart panel shows correct information
        """
        # Navigate to Top Collection and switch to Popular tab
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        top_collection.click_popular_tab()
        
        # Verify tab switched successfully
        assert top_collection.get_product_count() > 0, "Popular tab should show products"
        
        # Get product information before adding to cart
        product_name = top_collection.get_product_name(1)
        assert product_name, "Should be able to get product name from Popular tab"
        
        # Add product to cart
        top_collection.add_product_to_cart(1)
        
        # Wait for any potential navigation or loading
        # self.page.wait_for_load_state("networkidle", timeout=5000)
        
        # Check if notification appears - it might take time or might not appear if login required
        
        expect(self.home_page.notification.container).to_be_visible(timeout=5000)
        
        # Verify notification contains success message and product name
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message, got: {notification_message}"
        
        # Verify notification has action buttons
        expect(self.home_page.notification.view_cart_button).to_be_visible()
        expect(self.home_page.notification.checkout_button).to_be_visible()
        
        # Close notification
        self.home_page.notification.close()
        expect(self.home_page.notification.container).to_be_hidden()
        
        # Verify cart counter updated (this is the most reliable check)
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1 after adding product, got: {cart_count}"
        
        # Verify cart panel shows correct information
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        # Cart should not be empty anymore
        sub_total = self.home_page.cart_panel.get_sub_total()
        total = self.home_page.cart_panel.get_total()
        assert sub_total != "$0.00", f"Sub-total should not be $0.00, got: {sub_total}"
        assert total != "$0.00", f"Total should not be $0.00, got: {total}"

    def test_add_product_to_cart_from_latest_tab(self):
        """
        Test adding a product to cart from the LATEST tab.
        
        Steps:
        1. Navigate to Top Collection section
        2. Switch to LATEST tab
        3. Get product information before adding
        4. Add first product to cart
        5. Verify success notification and cart update
        6. Verify cart counter updated
        """
        # 1. Navigate to Top Collection and switch to Latest tab
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        
        # 2. Switch to Latest tab
        top_collection.click_latest_tab()
        assert top_collection.get_product_count() > 0, "Latest tab should show products"
        
        # 3. Get product information before adding to cart
        product_name = top_collection.get_product_name(24)
        assert product_name, "Should be able to get product name from Latest tab"
        
        # 4. Add product to cart using the convenience method
        top_collection.add_product_to_cart(24)
        
        # 5. Verify success notification appears
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        
        # Verify notification message contains product name
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message, got: {notification_message}"
        assert product_name in notification_message, f"Product name '{product_name}' should be in notification"
        
        # Close notification and verify cart counter
        self.home_page.notification.close()
        
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1 after adding product, got: {cart_count}"
        
        # Verify cart panel functionality
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        # Verify cart has content
        sub_total = self.home_page.cart_panel.get_sub_total()
        assert sub_total != "$0.00", f"Sub-total should not be $0.00 after adding product, got: {sub_total}"

    def test_add_product_to_cart_from_best_seller_tab(self):
        """
        Test adding a product to cart from the BEST SELLER tab.
        
        Steps:
        1. Navigate to Top Collection section
        2. Switch to BEST SELLER tab
        3. Get product information before adding
        4. Add first product to cart
        5. Verify success notification and cart update
        """
        # Navigate to Top Collection and switch to Best Seller tab
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        top_collection.click_best_seller_tab()
        
        # Verify tab switched successfully
        assert top_collection.get_product_count() > 0, "Best Seller tab should show products"
        
        # Get product information before adding to cart
        product_name = top_collection.get_product_name(48)
        assert product_name, "Should be able to get product name from Best Seller tab"
        
        # Add product to cart
        top_collection.add_product_to_cart(48)
        
        # Verify success notification appears
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        
        # Verify notification message
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message, got: {notification_message}"
        assert product_name in notification_message, f"Product name '{product_name}' should be in notification"
        
        # Close notification and verify cart state
        self.home_page.notification.close()
        
        # Verify cart counter updated
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1 after adding product, got: {cart_count}"

    def test_add_products_from_all_tabs_sequentially(self):
        """
        Test adding products from all three tabs (POPULAR, LATEST, BEST SELLER) sequentially.
        
        This test verifies:
        1. Products can be added from all tabs
        2. Cart counter accumulates correctly
        3. Each addition triggers proper notifications
        """
        top_collection = self.home_page.top_collection
        expected_cart_count = 0
        expected_total_price = 0
        added_products = []
                
        top_collection.click_popular_tab()
    
        # Get product information
        product_name = top_collection.get_product_name(1)
        product_price = top_collection.get_product_price(1)
        assert product_name, f"Should be able to get product name from POPULAR tab"
        added_products.append(product_name)
        
        # Add product to cart
        top_collection.add_product_to_cart(1)
        expected_cart_count += 1
        expected_total_price += product_price
        
        # Verify notification appears
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        
        # Verify notification message
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message for POPULAR tab"
        assert product_name in notification_message, f"Product name should be in notification for POPULAR tab"
        
        # Close notification
        self.home_page.notification.close()
        
        # Verify cart counter updates correctly
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == str(expected_cart_count), f"Cart count should be {expected_cart_count} after adding from {tab_name} tab, got: {cart_count}"
    

        top_collection.click_latest_tab()
        # Get product information
        product_name = top_collection.get_product_name(24)
        product_price = top_collection.get_product_price(24)
        added_products.append(product_name)
        
        # Add product to cart
        top_collection.add_product_to_cart(24)
        expected_cart_count += 1
        expected_total_price += product_price

        # Verify notification appears
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        
        # Verify notification message
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message for LATEST tab"
        assert product_name in notification_message, f"Product name should be in notification for LATEST tab"

        # Close notification
        self.home_page.notification.close()
        
        # Verify cart counter updates correctly
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == str(expected_cart_count), f"Cart count should be {expected_cart_count} after adding from {tab_name} tab, got: {cart_count}"



        top_collection.click_best_seller_tab()
        # Get product information
        product_name = top_collection.get_product_name(48)
        product_price = top_collection.get_product_price(48)
        added_products.append(product_name)

        # Add product to cart
        top_collection.add_product_to_cart(48)
        expected_cart_count += 1
        expected_total_price += product_price

        # Verify notification appears
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)

        # Verify notification message
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message for BEST SELLER tab"
        assert product_name in notification_message, f"Product name should be in notification for BEST SELLER tab"

        # Close notification
        self.home_page.notification.close()

        # Verify cart counter updates correctly
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == str(expected_cart_count), f"Cart count should be {expected_cart_count} after adding from {tab_name} tab, got: {cart_count}"

        # Final verification - check cart panel
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()

        # Cart should have accumulated value
        sub_total = self.home_page.cart_panel.get_sub_total()
        total = self.home_page.cart_panel.get_total()
        print(f"Sub-total: {sub_total}, Total: {total}")
        print(f"Expected total price: {expected_total_price}")

        assert sub_total != "$0.00", f"Sub-total should reflect added products, got: {sub_total}"
        assert total != "$0.00", f"Total should reflect added products, got: {total}"
        assert total == expected_total_price, f"Total should be {expected_total_price}, got: {total}"
        
        self.home_page.cart_panel.close_cart_panel()


        # Verify all products were added (final count should be 3)
        final_cart_count = self.home_page.header_actions.get_cart_count()
        assert final_cart_count == "3", f"Final cart count should be 3, got: {final_cart_count}"

    def test_add_multiple_products_from_same_tab(self):
        """
        Test adding multiple products from the same tab (POPULAR).
        
        This test verifies:
        1. Multiple products can be added from the same tab
        2. Cart counter accumulates correctly
        3. Each addition triggers proper notifications
        """
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        top_collection.click_popular_tab()
        
        # Verify we have at least 2 products to test with
        product_count = top_collection.get_product_count()
        assert product_count >= 2, f"Need at least 2 products in Popular tab for this test, found: {product_count}"
        
        # Add first product
        first_product_name = top_collection.get_product_name(1)
        top_collection.add_product_to_cart(1)
        
        # Verify first addition
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message and first_product_name in notification_message
        self.home_page.notification.close()
        
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1 after first product, got: {cart_count}"
        
        # Add second product
        second_product_name = top_collection.get_product_name(3)
        top_collection.add_product_to_cart(3)
        
        # Verify second addition
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message and second_product_name in notification_message
        self.home_page.notification.close()
        
        # Final verification
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "2", f"Cart count should be 2 after second product, got: {cart_count}"
        
        # Verify cart panel shows accumulated value
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        sub_total = self.home_page.cart_panel.get_sub_total()
        total = self.home_page.cart_panel.get_total()
        assert sub_total != "$0.00", f"Sub-total should reflect 2 products, got: {sub_total}"
        assert total != "$0.00", f"Total should reflect 2 products, got: {total}"

    def test_cart_panel_information_accuracy(self):
        """
        Test that cart panel displays accurate information after adding a product.
        
        This test focuses on verifying the cart panel functionality and information display.
        """
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        top_collection.click_popular_tab()
        expected_total_quantities = 0
        
        # Get product information before adding
        product_name = top_collection.get_product_name(1)
        product_price = top_collection.get_product_price(1)

        # Add product to cart
        top_collection.add_product_to_cart(1)
        expected_total_quantities += 1
        
        # Close notification
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        self.home_page.notification.close()
        
        # Open cart panel and verify its visibility
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        # Verify cart panel components are accessible
        assert self.home_page.cart_panel.is_visible(), "Cart panel should be visible"
        
        # Verify cart is no longer empty
        sub_total = self.home_page.cart_panel.get_sub_total()
        total = self.home_page.cart_panel.get_total()
        product_names = self.home_page.cart_panel.get_product_names()
        total_quantities = self.home_page.cart_panel.get_product_total_quantities()

        print(f"Product names: {product_names}")
        print(f"Product name: {product_name}")
        print(f"Product price: {product_price}")
        print(f"Sub-total: {sub_total}, Total: {total}")
        print(f"Total quantities: {total_quantities}")
        print(f"Expected total quantities: {expected_total_quantities}")
        assert product_name in product_names, f"Product name should be in cart panel: {product_names}"
        
        # Verify total quantities are correct
        # Both totals should be non-zero and properly formatted
        assert total_quantities == expected_total_quantities, f"Total quantities should be {expected_total_quantities}, got: {total_quantities}"
        assert sub_total != "$0.00", f"Sub-total should not be $0.00, got: {sub_total}"
        assert total != "$0.00", f"Total should not be $0.00, got: {total}"
        
        # Verify cart panel action buttons are available
        expect(self.home_page.cart_panel.edit_cart_button).to_be_visible()
        expect(self.home_page.cart_panel.checkout_button).to_be_visible()

    def test_notification_buttons_functionality(self):
        """
        Test that notification buttons (View Cart, Checkout) are functional after adding a product.
        
        This test verifies the notification component's action buttons work correctly.
        """
        top_collection = self.home_page.top_collection
        top_collection.scroll_to_top_collection()
        top_collection.click_popular_tab()
        
        # Add product to cart
        product_name = top_collection.get_product_name(1)
        top_collection.add_product_to_cart(1)
        
        # Verify notification appears with all expected elements
        expect(self.home_page.notification.container).to_be_visible(timeout=10000)
        
        # Verify notification content
        notification_message = self.home_page.notification.get_message_text()
        assert "Success:" in notification_message, f"Expected success message, got: {notification_message}"
        assert product_name in notification_message, f"Product name should be in notification: {notification_message}"
        
        # Verify both action buttons are visible and clickable
        expect(self.home_page.notification.view_cart_button).to_be_visible()
        expect(self.home_page.notification.checkout_button).to_be_visible()
        
        # Test View Cart button functionality
        # Note: We don't actually click it to avoid navigation, just verify it's functional
        view_cart_button = self.home_page.notification.view_cart_button
        assert view_cart_button.is_enabled(), "View Cart button should be enabled"
        
        checkout_button = self.home_page.notification.checkout_button
        assert checkout_button.is_enabled(), "Checkout button should be enabled"
        
        # Close notification using close button
        self.home_page.notification.close()
        expect(self.home_page.notification.container).to_be_hidden()
        
        # Verify cart counter updated correctly
        cart_count = self.home_page.header_actions.get_cart_count()
        assert cart_count == "1", f"Cart count should be 1, got: {cart_count}"