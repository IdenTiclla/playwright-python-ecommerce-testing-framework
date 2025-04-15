from pages.home_page import HomePage

def test_navbar_links(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_blog()
    assert page.url.endswith('/blog/home')
    assert page.url.startswith('https://ecommerce-playground.lambdatest.io/')
    assert page.url == 'https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/blog/home'

    
