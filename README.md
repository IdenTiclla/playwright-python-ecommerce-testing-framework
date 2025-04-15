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
│   ├── search_bar.py
│   └── navbar_horizontal.py
├── pages/
│   └── home_page.py
├── tests/
│   ├── search/
│   │   └── test_search.py
│   └── ...
├── conftest.py
├── README.md
└── ...
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
import pytest
from pages.home_page import HomePage

def test_search_functionality(page):
    home = HomePage(page)
    home.goto()
    home.search("iMac")
    page.wait_for_selector('.product-thumb')
    titles = page.locator('.product-thumb h4 a').all_text_contents()
    assert any("iMac" in title for title in titles)
```

### Example Page Object: HomePage

`pages/home_page.py`:
```python
from components.search_bar import SearchBar
from components.navbar_horizontal import NavbarHorizontal
class HomePage:
    URL = "https://ecommerce-playground.lambdatest.io/"
    def __init__(self, page):
        self.page = page
        self.search_bar = SearchBar(page)
        self.navbar_horizontal = NavbarHorizontal(page)
    def goto(self):
        self.page.goto(self.URL)
    def search(self, term):
        self.search_bar.search(term)
```

### Example Component: SearchBar

`components/search_bar.py`:
```python
class SearchBar:
    SEARCH_INPUT = 'input[name="search"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    def __init__(self, page):
        self.page = page
    def search(self, term):
        self.page.fill(self.SEARCH_INPUT, term)
        self.page.click(self.SEARCH_BUTTON)
```

### Pytest Fixtures

`conftest.py`:
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
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