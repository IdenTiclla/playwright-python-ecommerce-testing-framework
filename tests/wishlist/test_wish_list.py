from playwright.sync_api import expect
from tests.base_test import BaseTest

class TestWishList(BaseTest):
    def test_add_to_wishlist_from_top_products(self):
        # home_page.goto()
        self.home_page.goto()
        self.page.wait_for_timeout(1000)

        self.home_page.top_products.scroll_to_top_products()
        # expect(home_page.top_products.section).to_be_visible(timeout=10000)

        # Esperar a que el dom este cargado
        self.page.wait_for_load_state("domcontentloaded")

        # verificar que la seccion de productos top esta visible
        assert self.page.locator(self.home_page.top_products.section).is_visible(timeout=10000), "Top products section should be visible"
        self.page.wait_for_timeout(1000)

        self.home_page.top_products.add_product_to_wishlist(index=0)
        self.page.wait_for_timeout(1000)

        # verificar que se muestra la notificacion
        expect(self.page.locator(self.home_page.notification.container)).to_be_visible(timeout=10000)
        # notification_title = page.locator(home_page.notification.title).text_content()
        notification_title = self.home_page.notification.get_title_text()
        # notification_message = page.locator(home_page.notification.message).text_content()
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
        expect(self.page.locator(self.home_page.notification.container)).not_to_be_visible(timeout=10000)

    
    def test_add_to_wishlist_from_quick_view(self):
        self.home_page.goto()
        self.page.wait_for_timeout(1000)

        # esperar a que el dom este cargado
        self.page.wait_for_load_state("domcontentloaded")

        self.home_page.top_products.scroll_to_top_products()
        
        expect(self.page.locator(self.home_page.top_products.section)).to_be_visible(timeout=10000)

        self.home_page.top_products.show_quick_view(index=0)
        self.page.wait_for_timeout(1000)

        expect(self.page.locator(self.home_page.quick_view_modal.container)).to_be_visible(timeout=10000)

        self.home_page.quick_view_modal.add_to_wishlist()

        expect(self.page.locator(self.home_page.notification.container)).to_be_visible(timeout=10000)

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
        expect(self.page.locator(self.home_page.notification.container)).not_to_be_visible(timeout=10000)