# Practicing Playwright Python

## Description
This project demonstrates best practices for browser automation using Playwright in Python, following a maintainable structure with the Page Object Model (POM) and reusable components. The project is configured to automate the demo e-commerce site: https://ecommerce-playground.lambdatest.io/

## Requirements
- Python >= 3.12
- `uv` package manager (optional but recommended)

## Installation

### For Windows Users
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd practicing-playwright-python
   ```
2. **Install `uv`**:
   ```powershell
   (Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing).Content | powershell
   ```
3. **Create a virtual environment**:
   ```powershell
   uv venv
   ```
4. **Activate the virtual environment**:
   ```powershell
   .venv\Scripts\activate
   ```
5. **Install Playwright**:
   ```powershell
   uv pip install playwright
   ```
6. **Install the required browsers**:
   ```powershell
   playwright install
   ```

### For macOS/Ubuntu Users
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd practicing-playwright-python
   ```
2. **Install `uv`**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Create a virtual environment**:
   ```bash
   uv venv
   ```
4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```
5. **Install Playwright**:
   ```bash
   uv pip install playwright
   ```
6. **Install the required browsers**:
   ```bash
   playwright install
   ```

## Project Structure

```
practicing-playwright-python/
├── components/
│   ├── alert.py
│   ├── base_component.py
│   ├── carousel.py
│   ├── cart_panel.py
│   ├── header_actions.py
│   ├── navbar_horizontal.py
│   ├── notification.py
│   ├── quick_view_modal.py
│   ├── search_bar.py
│   ├── sidebar_navigation.py
│   ├── top_collection.py
│   └── top_products.py
├── pages/
│   ├── account_edit_page.py
│   ├── account_page.py
│   ├── base_page.py
│   ├── cart_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── search_page.py
│   ├── shopping_cart_page.py
│   ├── success_page.py
│   └── wishlist_page.py
├── tests/
│   ├── auth/
│   │   ├── test_account_edit.py
│   │   ├── test_login.py
│   │   └── test_register.py
│   ├── base_test.py
│   ├── carousel/
│   ├── cart/
│   ├── navbar_horizontal/
│   ├── quick_view/
│   ├── search/
│   │   └── test_search.py
│   └── wishlist/
├── conftest.py
├── pyproject.toml
├── README.md
└── uv.lock
```

- **components/**: Reusable UI components (e.g., search bar, navbar).
- **pages/**: Page Object Model classes for each page (e.g., HomePage).
- **tests/**: Test cases, organized by feature.
- **conftest.py**: Pytest fixtures for Playwright setup.

## Usage

### Running Tests

1. **Run all tests:**
   ```bash
   pytest
   ```
2. **Run a specific test file:**
   ```bash
   pytest tests/search/test_search.py
   ```

### Example Test: Search Functionality

`tests/search/test_search.py`:
```python
class TestSearch:
    @pytest.fixture
    def search_page(self, page: Page) -> SearchPage:
        return SearchPage(page)
    
    @pytest.fixture
    def home_page(self, page: Page) -> HomePage:
        return HomePage(page)

    def test_search_functionality(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iMac")
        
        search_page.page.wait_for_load_state("domcontentloaded")
        count = search_page.page.locator(search_page.product_titles).count()
        assert count > 0, "Expected at least one search result"

        results = search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"
```

### Example Page Object: HomePage

`pages/home_page.py`:
```python
from playwright.sync_api import Page
from pages.base_page import BasePage
from components.search_bar import SearchBar
from components.navbar_horizontal import NavbarHorizontal
from components.carousel import Carousel
from components.top_collection import TopCollection
from components.top_products import TopProducts

class HomePage(BasePage):
    URL = "https://ecommerce-playground.lambdatest.io/"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_bar = SearchBar(page)
        self.navbar_horizontal = NavbarHorizontal(page)
        self.carousel = Carousel(page)
        self.top_collection = TopCollection(page)
        self.top_products = TopProducts(page)
        
    def goto(self) -> None:
        """
        Navigate to the home page
        """
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
```

### Example Component: SearchBar

`components/search_bar.py`:
```python
from playwright.sync_api import Page, Locator
from components.base_component import BaseComponent

class SearchBar(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self._search_input = 'input[name="search"]'
        self._search_button = 'button[type="submit"]'
        
    @property
    def search_input(self) -> Locator:
        return self.page.locator(self._search_input)
        
    @property 
    def search_button(self) -> Locator:
        return self.page.locator(self._search_button)

    def perform_search(self, text: str) -> None:
        """
        Performs a search using the search bar
        Args:
            text: The text to search for
        """
        self.search_input.fill(text)
        self.search_button.click()
        self.page.wait_for_load_state("domcontentloaded")
```

### Pytest Fixtures

`conftest.py`:
```python
import pytest
from playwright.sync_api import sync_playwright, Page, Browser
from typing import Generator

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """
    Creates a browser instance that is shared across all tests in the session.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser) -> Generator[Page, None, None]:
    """
    Creates a new page for each test.
    
    Args:
        browser: The browser instance to create the page in
        
    Returns:
        Generator[Page, None, None]: The page instance
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
```

## Headless Mode
To run tests in headless mode (no browser window), set `headless=True` in `conftest.py` when launching the browser.

## Updating Browsers
To update the browsers that Playwright will automate, run:
```bash
playwright install
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.