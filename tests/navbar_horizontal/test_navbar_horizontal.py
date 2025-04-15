from pages.home_page import HomePage

def test_navbar_links(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_blog()
    assert page.url.endswith('/blog/home')
    assert page.url.startswith('https://ecommerce-playground.lambdatest.io/')
    assert page.url == 'https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/blog/home'

    

def test_navbar_horizontal_special_hot(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_special_hot()
    assert page.url == 'https://ecommerce-playground.lambdatest.io/index.php?route=product/special'
    assert page.url.startswith('https://ecommerce-playground.lambdatest.io/')
    assert page.url.endswith('route=product/special')

def test_navbar_horizontal_home_page(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_home_page()
    assert page.url == 'https://ecommerce-playground.lambdatest.io/index.php?route=common/home'
    assert page.url.startswith('https://ecommerce-playground.lambdatest.io/')
    assert page.url.endswith('route=common/home')
