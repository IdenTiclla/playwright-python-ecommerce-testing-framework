# Wishlist Page Tests

This directory contains comprehensive tests for the Wishlist Page functionality of the e-commerce playground application.

## 📁 Files Overview

### `test_wishlist_page.py`
**NEW** - Comprehensive test suite for the Wishlist Page using the new Page Object Model.

**Test Coverage:**
- ✅ Page navigation and URL verification
- ✅ Page elements visibility and layout
- ✅ Table headers and structure validation
- ✅ Product details display and formatting
- ✅ Product navigation (clicking product links)
- ✅ Add to cart functionality from wishlist
- ✅ Remove products from wishlist
- ✅ Sidebar navigation links
- ✅ Continue button functionality
- ✅ Stock status display
- ✅ Empty wishlist state handling
- ✅ Responsive design testing

### `test_wish_list.py`
**EXISTING** - Original wishlist tests focusing on adding products to wishlist from home page.

**Test Coverage:**
- ✅ Add to wishlist from top products (without login - shows login prompt)
- ✅ Add to wishlist from quick view modal (without login - shows login prompt)

## 🏗️ Page Object Model

### `pages/wishlist_page.py`
**NEW** - Complete Page Object Model for the Wishlist Page.

**Key Features:**
- **Navigation methods**: Direct page navigation and URL handling
- **Element interaction**: Table manipulation, product actions, sidebar navigation
- **Data extraction**: Product details, prices, stock status, counts
- **Validation helpers**: Check product presence, button states, page elements
- **Responsive support**: Works across different viewport sizes

**Main Methods:**
```python
# Navigation
wishlist_page.goto()
wishlist_page.wait_for_page_load()

# Product Information
product_details = wishlist_page.get_product_details(0)
items_count = wishlist_page.get_wishlist_items_count()
is_present = wishlist_page.is_product_in_wishlist("iMac")

# Product Actions
wishlist_page.add_to_cart(0)
wishlist_page.remove_from_wishlist(0)
wishlist_page.click_product_name(0)

# Page Navigation
wishlist_page.click_continue()
wishlist_page.click_my_account()
wishlist_page.logout()
```

## 🚀 Running the Tests

### Quick Start
```bash
# Run all wishlist page tests
python -m pytest tests/wishlist/test_wishlist_page.py -v

# Run specific test
python -m pytest tests/wishlist/test_wishlist_page.py::TestWishlistPage::test_wishlist_page_navigation -v

# Run with test runner script
python run_wishlist_tests.py
```

### Advanced Options
```bash
# Run in headful mode (see browser)
python -m pytest tests/wishlist/test_wishlist_page.py --headed

# Run with HTML report
python -m pytest tests/wishlist/test_wishlist_page.py --html=reports/wishlist_report.html

# Run with slow motion for debugging
python -m pytest tests/wishlist/test_wishlist_page.py --slowmo 1000

# Run with specific browser
python -m pytest tests/wishlist/test_wishlist_page.py --browser firefox
```

## 🧪 Test Scenarios

### 1. Basic Page Functionality
- **Navigation**: Direct URL access and page loading
- **Elements**: Verify all page elements are visible and functional
- **Layout**: Check table structure and headers

### 2. Product Management
- **Display**: Verify product information is correctly shown
- **Actions**: Test add to cart and remove from wishlist
- **Navigation**: Test clicking product links

### 3. User Interactions
- **Sidebar**: Test all sidebar navigation links
- **Buttons**: Verify continue button and action buttons
- **Responsive**: Test across different screen sizes

### 4. Data Validation
- **Product Details**: Verify all product fields are present
- **Price Format**: Check price formatting and currency
- **Stock Status**: Validate stock status display

## 📋 Prerequisites

### User Account
Most tests require a logged-in user. The tests use these credentials:
- **Email**: `john.doe.test@example.com`
- **Password**: `TestPassword123!`

**Note**: Make sure this account exists or modify the credentials in the test files.

### Dependencies
```bash
# Install required packages
pip install playwright pytest pytest-html

# Install browser binaries
playwright install
```

## 🔧 Test Configuration

### Fixtures Used
- `wishlist_page`: WishlistPage instance
- `home_page`: HomePage instance for setup
- `login_page`: LoginPage instance for authentication
- `page`: Playwright page instance

### Test Data
Tests use the existing product data from the e-commerce site:
- **iMac** products from Top Products section
- **Price range**: $122.00 - $170.00
- **Stock statuses**: "In Stock", "Out Of Stock", "Pre-Order"

## 🐛 Troubleshooting

### Common Issues

1. **Login Required Errors**
   - Ensure test user account exists
   - Check credentials in test files
   - Verify login functionality works

2. **Element Not Found**
   - Check if page structure has changed
   - Update selectors in `wishlist_page.py`
   - Add wait conditions if needed

3. **Empty Wishlist**
   - Some tests skip if wishlist is empty
   - Add products to wishlist before running tests
   - Use setup methods to ensure test data

### Debug Mode
```bash
# Run with debug output
python -m pytest tests/wishlist/test_wishlist_page.py -v -s

# Run single test with browser visible
python -m pytest tests/wishlist/test_wishlist_page.py::TestWishlistPage::test_wishlist_page_navigation --headed --slowmo 1000
```

## 📈 Test Metrics

### Coverage Areas
- **UI Elements**: 100% of visible elements tested
- **User Actions**: All clickable elements and forms
- **Data Validation**: Product information and formatting
- **Navigation**: All internal and external links
- **Responsive**: Desktop, tablet, and mobile viewports

### Test Types
- **Functional Tests**: Core wishlist functionality
- **UI Tests**: Element visibility and layout
- **Integration Tests**: Cross-page navigation
- **Responsive Tests**: Multi-viewport validation

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Wishlist Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: python -m pytest tests/wishlist/test_wishlist_page.py --html=reports/wishlist.html
```

## 📝 Contributing

When adding new wishlist tests:

1. **Follow the existing pattern** in `test_wishlist_page.py`
2. **Use the POM methods** from `wishlist_page.py`
3. **Add proper documentation** and comments
4. **Include assertions** for all validations
5. **Handle edge cases** (empty wishlist, login required, etc.)
6. **Test across browsers** and viewport sizes

## 📚 Related Documentation

- [Main Project README](../../README.md)
- [Page Objects Documentation](../../pages/README.md)
- [Test Configuration](../../conftest.py)
- [Playwright Documentation](https://playwright.dev/python/) 