# Playwright Python E-commerce Test Automation Framework

## Description
This project demonstrates best practices for browser automation using Playwright in Python, following a maintainable structure with the Page Object Model (POM) and reusable components. Features include parallel test execution, custom test markers, and automated test orchestration. The project is configured to automate the demo e-commerce site: https://ecommerce-playground.lambdatest.io/

## Requirements
- Python >= 3.12
- `uv` package manager (recommended for dependency management)
- Playwright >= 1.51.0

## Installation

### Quick Setup (Recommended)
Using the provided Makefile:
```bash
git clone https://github.com/IdenTiclla/playwright-python-ecommerce-testing-framework.git
cd playwright-python-ecommerce-testing-framework
make install
```

### Manual Installation

#### For Windows Users
1. **Clone the repository**:
   ```bash
   git clone https://github.com/IdenTiclla/playwright-python-ecommerce-testing-framework.git
   cd playwright-python-ecommerce-testing-framework
   ```
2. **Install `uv`**:
   ```powershell
   (Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing).Content | powershell
   ```
3. **Install dependencies**:
   ```powershell
   uv sync
   ```
4. **Install browsers**:
   ```powershell
   playwright install chromium
   ```

#### For macOS/Ubuntu Users
1. **Clone the repository**:
   ```bash
   git clone https://github.com/IdenTiclla/playwright-python-ecommerce-testing-framework.git
   cd playwright-python-ecommerce-testing-framework
   ```
2. **Install `uv`**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Install dependencies**:
   ```bash
   uv sync
   ```
4. **Install browsers**:
   ```bash
   playwright install chromium
   ```

## Project Structure

```
practicing-playwright-python/
├── components/                 # Reusable UI components
│   ├── alert.py
│   ├── base_component.py      # Base class for all components
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
├── pages/                     # Page Object Model classes
│   ├── account_edit_page.py
│   ├── account_page.py
│   ├── base_page.py           # Base class for all pages
│   ├── home_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── search_page.py
│   ├── shopping_cart_page.py
│   ├── success_page.py
│   └── wishlist_page.py
├── tests/                     # Test cases organized by feature
│   ├── auth/                  # Authentication tests
│   │   ├── test_account_edit.py
│   │   ├── test_login.py
│   │   └── test_register.py
│   ├── base_test.py          # Base test class with common setup
│   ├── carousel/             # Carousel component tests
│   │   └── test_main_carousel.py
│   ├── cart/                 # Shopping cart tests
│   │   ├── test_cart.py
│   │   └── top_collection/
│   │       └── test_add_to_cart.py
│   ├── navbar_horizontal/    # Navigation bar tests
│   │   └── test_navbar_horizontal.py
│   ├── quick_view/          # Quick view modal tests
│   │   └── test_quick_view.py
│   ├── search/              # Search functionality tests
│   │   └── test_search.py
│   └── wishlist/            # Wishlist tests
│       └── test_wish_list.py
├── utils/                   # Utility modules
│   ├── config.py           # Configuration management
│   └── data_generator.py   # Test data generation
├── conftest.py             # Pytest fixtures and configuration
├── Makefile               # Build and test automation
├── main.py               # Entry point script
├── pyproject.toml        # Project dependencies and configuration
├── README_PARALLEL.md    # Parallel execution documentation
├── run_tests.py         # Advanced test runner with parallel support
└── uv.lock             # Dependency lock file
```

## Key Features

- **Page Object Model (POM)**: Maintainable test structure with clear separation of concerns
- **Reusable Components**: Modular UI components for consistent interactions
- **Parallel Test Execution**: Optimized test runs with configurable parallelism
- **Custom Test Markers**: Organized test categorization (cart, auth, slow, etc.)
- **Automated Test Orchestration**: Smart test runner with automatic parallel/sequential detection
- **Data Generation**: Faker integration for realistic test data
- **Configuration Management**: Centralized configuration and environment handling

## Usage

### Running Tests with Makefile (Recommended)

1. **Run all tests (auto-detect mode):**
   ```bash
   make test
   ```

2. **Run specific test categories:**
   ```bash
   make test-auth        # Authentication tests
   make test-cart        # Shopping cart tests
   make test-navbar      # Navigation tests
   make test-fast        # Quick tests (excludes slow markers)
   ```

3. **Parallel vs Sequential execution:**
   ```bash
   make test-parallel    # Force parallel execution
   make test-sequential  # Force sequential execution
   ```

4. **Custom test execution:**
   ```bash
   make test-custom TESTS=tests/auth/ WORKERS=4
   make test-custom TESTS=tests/cart/test_cart.py MARKERS='not slow'
   ```

### Running Tests with pytest

1. **Run all tests:**
   ```bash
   pytest
   ```

2. **Run with parallel execution:**
   ```bash
   pytest -n auto  # Auto-detect CPU cores
   pytest -n 4     # Use 4 workers
   ```

3. **Run specific test markers:**
   ```bash
   pytest -m "cart"           # Only cart tests
   pytest -m "not slow"       # Exclude slow tests
   pytest -m "auth or cart"   # Auth OR cart tests
   ```

4. **Run specific test files:**
   ```bash
   pytest tests/search/test_search.py
   pytest tests/auth/        # All auth tests
   ```

## Available Test Markers

The project uses custom pytest markers for test organization:

- **`cart`**: Tests related to shopping cart functionality
- **`auth`**: Authentication and user account tests  
- **`navbar_horizontal`**: Horizontal navigation bar tests
- **`quick_view_modal`**: Quick view modal tests
- **`slow`**: Tests that take longer to execute
- **`parallel`**: Tests that can run in parallel safely
- **`serial`**: Tests that must run sequentially

## Configuration

### pyproject.toml
Key configuration options:
- **Parallel execution**: Configured via `pytest-xdist`
- **Test markers**: Custom markers for test categorization
- **Timeouts**: 300-second timeout to prevent hanging tests
- **Dependencies**: Playwright, pytest, Faker, python-dotenv

### Environment Configuration
The project supports environment-based configuration through `utils/config.py` and `.env` files for different test environments.

## Advanced Test Execution

### Using run_tests.py
The project includes a sophisticated test runner that automatically optimizes test execution:

```bash
# Auto-detect parallel/sequential based on test markers
python run_tests.py auto

# Force parallel execution with auto-detected workers
python run_tests.py parallel

# Force sequential execution
python run_tests.py sequential

# Custom parallel execution with specific workers
python run_tests.py parallel 4 tests/cart/

# Run with custom markers
python run_tests.py parallel auto tests/ "not slow"
```

### Makefile Commands Summary
```bash
make help           # Show all available commands
make install        # Install dependencies and browsers
make test          # Auto-detect optimal test execution
make test-fast     # Quick tests (excludes slow)
make check         # Verify system configuration
make clean         # Remove temporary files
```

## Best Practices

### Test Organization
- **Use descriptive test names** that clearly indicate what is being tested
- **Group related tests** using custom markers (`@pytest.mark.cart`, `@pytest.mark.auth`)
- **Leverage parallel execution** for independent tests to reduce overall test time
- **Mark slow tests** appropriately to allow for selective execution

### Page Object Model
- **Inherit from BasePage** for consistent behavior across all pages
- **Use BaseComponent** for reusable UI elements
- **Encapsulate page-specific logic** within page objects
- **Return meaningful objects** from page actions for method chaining

### Test Data Management
- **Use Faker** for generating realistic test data
- **Centralize configuration** in `utils/config.py`
- **Environment-specific settings** via environment variables

## Parallel Execution Notes

- Tests marked with `@pytest.mark.serial` will always run sequentially
- Tests marked with `@pytest.mark.parallel` are optimized for parallel execution
- The `run_tests.py` automatically detects the best execution strategy
- Use `make test-fast` to skip slow tests during development

## Troubleshooting

### Common Issues
1. **Browser installation**: Run `playwright install chromium`
2. **Permission errors**: Ensure proper virtual environment activation
3. **Port conflicts**: Check if other services are using default ports
4. **Slow tests**: Use `make test-fast` to exclude slow markers

### System Requirements Check
```bash
make check  # Verify Python, Playwright, and system configuration
```

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate test markers to new tests
3. Update documentation for new features
4. Ensure tests pass both sequentially and in parallel
5. Use meaningful commit messages

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.