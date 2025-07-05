import time
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from playwright.sync_api import expect
import pytest
import re

class TestCart:
    @pytest.fixture
    def home_page(self, page) -> HomePage:
        return HomePage(page)
    
    @pytest.fixture
    def register_page(self, page) -> RegisterPage:
        return RegisterPage(page)

    def test_empty_cart_with_new_user(self, home_page, register_page, page):
        home_page.goto()
        home_page.navbar_horizontal.click_my_account_option("Register")

        register_page.register(
            firstname="Brayan",
            lastname="Mendoza",
            email="test.user" + str(int(time.time())) + "@example.com",
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@123",  # Same password for confirmation
            subscribe_newsletter=True
        )
        # assert cart panel is not visible 
        assert not home_page.cart_panel.is_visible(), "Cart panel should not be visible" 
        home_page.click_on_my_cart_button()
        page.wait_for_load_state("domcontentloaded")
        assert home_page.cart_panel.is_visible(), "Cart panel should be visible"

        # Opción 1: Usar expect (Playwright)
        expect(home_page.page.locator(home_page.cart_panel.sub_total)).to_have_text("$0.00")
        expect(home_page.page.locator(home_page.cart_panel.total)).to_have_text("$0.00")
        expect(home_page.page.locator(home_page.cart_panel.message)).to_have_text("Your shopping cart is empty!")

        # Opción 2: Usar assert con inner_text()
        assert home_page.page.locator(home_page.cart_panel.sub_total).inner_text() == "$0.00", "Sub total should be $0.00"
        assert home_page.page.locator(home_page.cart_panel.total).inner_text() == "$0.00", "Total should be $0.00"
        assert home_page.page.locator(home_page.cart_panel.message).inner_text() == "Your shopping cart is empty!", "Cart message should indicate empty cart"

        # Opción 3: Usar text_content() (puede devolver None si no existe el elemento)
        assert home_page.page.locator(home_page.cart_panel.sub_total).text_content() == "$0.00"
        assert home_page.page.locator(home_page.cart_panel.total).text_content() == "$0.00"
        assert home_page.page.locator(home_page.cart_panel.message).text_content() == "Your shopping cart is empty!"

        # Opción 4: Usar métodos de la clase CartPanel
        assert home_page.cart_panel.check_message("Your shopping cart is empty!") == True
        assert home_page.cart_panel.check_sub_total("$0.00") == True
        assert home_page.cart_panel.check_total("$0.00") == True

    def test_adding_product_to_cart_with_new_user(self, home_page, register_page, page):
        # Configuración: navegar a la página y esperar carga completa
        home_page.goto()
        page.wait_for_load_state("networkidle")
        
        # Registro: navegar a la página de registro
        home_page.navbar_horizontal.click_my_account_option("Register")
        page.wait_for_load_state("networkidle")
        
        # Crear un email único con timestamp para evitar conflictos
        unique_email = f"test.user{int(time.time())}@example.com"
        
        # Completar registro con datos del usuario
        register_page.register(
            firstname="Brayan",
            lastname="Mendoza",
            email=unique_email,
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@123",  # Mismo password para confirmación
            subscribe_newsletter=True
        )
        
        # Esperar a que se complete el registro completamente
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(".*account/success"), timeout=10000)
        
        # Volver a la página principal de forma explícita
        home_page.goto()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_title(re.compile("Your Store"), timeout=5000)

        # try:
        #     # Cerrar cualquier modal o popup que pueda interferir
        #     if page.locator("button.mfp-close").is_visible():
        #         page.locator("button.mfp-close").click()
        # except:
        #     # Ignorar errores si no hay modal para cerrar
        #     pass
            
        # Asegurar que la sección de productos principales es visible
        home_page.top_products.scroll_to_top_products()
        page.wait_for_timeout(1000)  # Pequeña pausa para asegurar que la UI está estable
        expect(page.locator(home_page.top_products.section)).to_be_visible(timeout=10000)
        
        # Añadir el primer producto al carrito con manejo adecuado
        home_page.top_products.add_product_to_cart(index=0)
        
        # Esperar a la notificación de éxito (ajustar selector según la implementación real)
        notification = page.locator(home_page.notification.container)
        expect(notification).to_be_visible(timeout=5000)

        # verificar el mensaje de notificación
        message = home_page.notification.get_message_text()
        # assert message == "Success: You have added MacBook Pro to your shopping cart!", "Message should be 'Success: You have added MacBook Pro to your shopping cart!'"
        assert "Success" in message, "Message should contain 'Success'"
        assert message == "Success: You have added iMac to your shopping cart!", "Message should be 'Success: You have added iMac to your shopping cart!'"



        view_cart_button = page.locator(home_page.notification.view_cart_button)
        expect(view_cart_button).to_be_visible(timeout=5000)


        checkout_button = page.locator(home_page.notification.checkout_button)
        expect(checkout_button).to_be_visible(timeout=5000)


        # Cerrar la notificación
        close_button = page.locator(home_page.notification.close_button)
        expect(close_button).to_be_visible(timeout=5000)
        close_button.click()
        expect(notification).not_to_be_visible(timeout=5000)

            
        
        # Verificar el carrito: hacer clic y verificar contenido
        home_page.click_on_my_cart_button()
        expect(page.locator(home_page.cart_panel.panel)).to_be_visible(timeout=5000)
        
        # Verificar que el panel del carrito está visible
        assert home_page.cart_panel.is_visible(), "Cart panel should be visible"
        
        # Verificar que NO muestra el mensaje de carrito vacío
        expect(page.locator(home_page.cart_panel.message)).not_to_be_visible(timeout=3000)
        
        # Verificar contenido del carrito (usar soft assertions para ver todos los problemas)
        sub_total_locator = page.locator(home_page.cart_panel.sub_total)
        total_locator = page.locator(home_page.cart_panel.total)
        
        # Esperar a que se actualicen los valores con tiempos de espera adecuados
        expect(sub_total_locator).to_be_visible(timeout=5000)
        expect(total_locator).to_be_visible(timeout=5000)
        
        # Verificar que los valores no sean $0.00 (esto es mínimo, idealmente verificar valores exactos)
        sub_total_text = sub_total_locator.text_content()
        total_text = total_locator.text_content()
        
        assert "$0.00" not in sub_total_text, f"Sub total should not be $0.00, got: {sub_total_text}"
        assert "$0.00" not in total_text, f"Total should not be $0.00, got: {total_text}"
        
        assert "$140.00" in sub_total_text, f"Sub total should be $140.00, got: {sub_total_text}"
        assert "$170.00" in total_text, f"Total should be $170.00, got: {total_text}"

