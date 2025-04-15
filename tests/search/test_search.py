import pytest
from pages.home_page import HomePage

def test_search_functionality(page):
    home = HomePage(page)
    home.goto()
    home.search("iMac")
    page.wait_for_selector('.product-thumb')
    titles = page.locator('.product-thumb h4 a').all_text_contents()
    assert any("iMac" in title for title in titles)