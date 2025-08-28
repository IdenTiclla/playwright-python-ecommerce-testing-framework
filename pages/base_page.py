from playwright.sync_api import Page
from components.navbar_horizontal import NavbarHorizontal
from components.search_bar import SearchBar
from components.alert import Alert
from components.sidebar_navigation import SidebarNavigation
from components.cart_panel import CartPanel
class BasePage:
    """
    La clase base para todos los Page Objects.
    Contiene elementos y funcionalidades comunes a todas las páginas.
    """
    def __init__(self, page: Page):
        self.page = page
        # Componentes comunes que aparecen en la mayoría de las páginas
        self.navbar_horizontal = NavbarHorizontal(page)
        self.search_bar = SearchBar(page)
        self.alert_component = Alert(page)
        self.sidebar_navigation_component = SidebarNavigation(page)
        self.cart_panel = CartPanel(page)

    def _visit(self, url: str):
        """Navega a una URL específica."""
        self.page.goto(url, wait_until="domcontentloaded")

    def wait_for_page_load(self, state: str = "domcontentloaded"):
        """Espera a que la página alcance un estado de carga específico."""
        self.page.wait_for_load_state(state)

    def get_title(self) -> str:
        """Obtiene el título de la página."""
        return self.page.title()