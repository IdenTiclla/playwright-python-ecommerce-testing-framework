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


def test_megamenu_options(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_megamenu_option("Apple")
    # assert start with
    assert page.url.startswith("https://ecommerce-playground.lambdatest.io")
    # assert url is equal to
    assert page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=product/manufacturer/info&manufacturer_id=8"
    # assert end with
    assert page.url.endswith("route=product/manufacturer/info&manufacturer_id=8")   
    assert page.title() == "Apple"

    # wait for the page to load
    page.wait_for_load_state("domcontentloaded")

    home.navbar_horizontal.click_megamenu_option("HTC")
    # assert start with
    assert page.url.startswith("https://ecommerce-playground.lambdatest.io")
    # assert url is equal to
    assert page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=product/manufacturer/info&manufacturer_id=5"
    # assert end with
    assert page.url.endswith("route=product/manufacturer/info&manufacturer_id=5")
    assert page.title() == "HTC"

    # wait for the page to load
    page.wait_for_load_state("domcontentloaded")

    home.navbar_horizontal.click_megamenu_option("LG")
    # assert start with
    assert page.url.startswith("https://ecommerce-playground.lambdatest.io")
    # assert url is equal to
    assert page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=product/manufacturer/info&manufacturer_id=8"
    # assert end with
    assert page.url.endswith("route=product/manufacturer/info&manufacturer_id=8")

    