import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.search_page import SearchPage
from pages.account_page import AccountPage
from pages.account_edit_page import AccountEditPage
from pages.wishlist_page import WishListPage
from pages.success_page import SuccessPage
from pages.account_edit_page import AccountEditPage
from pages.shopping_cart_page import ShoppingCartPage


@pytest.mark.usefixtures("page")
class BaseTest:
    """
    Clase base para los tests. Cualquier clase de test que herede de BaseTest
    tendrá acceso automático a la fixture 'page' de Playwright.
    """

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.register_page = RegisterPage(page)
        self.search_page = SearchPage(page)
        self.account_page = AccountPage(page)
        self.account_edit_page = AccountEditPage(page)
        self.wishlist_page = WishListPage(page)
        self.success_page = SuccessPage(page)
        self.shopping_cart_page = ShoppingCartPage(page)

    # El teardown lo maneja conftest.py - no necesitamos duplicarlo aquí
