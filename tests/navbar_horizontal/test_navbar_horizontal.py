import pytest
from tests.base_test import BaseTest
from utils.config import BASE_URL

@pytest.mark.navbar_horizontal
class TestNavbarHorizontal(BaseTest):

    def test_navbar_links(self):
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_blog()
        assert self.page.url.endswith('/blog/home')
        assert self.page.url.startswith(f'{BASE_URL}/')
        assert self.page.url == f'{BASE_URL}/index.php?route=extension/maza/blog/home'

    

    def test_navbar_horizontal_special_hot(self):
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_special_hot()
        assert self.page.url == f'{BASE_URL}/index.php?route=product/special'
        assert self.page.url.startswith(f'{BASE_URL}/')
        assert self.page.url.endswith('route=product/special')

    def test_navbar_horizontal_home_page(self):
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_home_page()
        assert self.page.url == f'{BASE_URL}/index.php?route=common/home'
        assert self.page.url.startswith(f'{BASE_URL}/')
        assert self.page.url.endswith('route=common/home')


    def test_megamenu_options(self):
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_megamenu_option("Apple")
        # assert start with
        assert self.page.url.startswith(f"{BASE_URL}")
        # assert url is equal to
        assert self.page.url == f"{BASE_URL}/index.php?route=product/manufacturer/info&manufacturer_id=8"
        # assert end with
        assert self.page.url.endswith("route=product/manufacturer/info&manufacturer_id=8")   
        assert self.page.title() == "Apple"

        # wait for the page to load
        self.page.wait_for_load_state("domcontentloaded")

        self.home_page.navbar_horizontal.click_megamenu_option("HTC")
        # assert start with
        assert self.page.url.startswith(f"{BASE_URL}")
        # assert url is equal to
        assert self.page.url == f"{BASE_URL}/index.php?route=product/manufacturer/info&manufacturer_id=5"
        # assert end with
        assert self.page.url.endswith("route=product/manufacturer/info&manufacturer_id=5")
        assert self.page.title() == "HTC"

        # wait for the page to load
        self.page.wait_for_load_state("domcontentloaded")

        self.home_page.navbar_horizontal.click_megamenu_option("LG")
        # assert start with
        assert self.page.url.startswith(f"{BASE_URL}")
        # assert url is equal to
        assert self.page.url == f"{BASE_URL}/index.php?route=product/manufacturer/info&manufacturer_id=8"
        # assert end with
        assert self.page.url.endswith("route=product/manufacturer/info&manufacturer_id=8")

        
    def test_shop_by_category(self):
        self.home_page.goto()
        
        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Components")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=25"
        

        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Cameras")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=33"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Phone, Tablets & Ipod")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=57"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("MP3 Players")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=34"



        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Laptops & Notebooks")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=18"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Desktops and Monitors")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=28"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Printers & Scanners")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=30"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Mice and Trackballs")
        assert self.page.url == f"{BASE_URL}/index.php?route=product/category&path=29"


        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Fashion and Accessories")
        assert self.page.url == f"{BASE_URL}/"
        

        self.page.wait_for_load_state("domcontentloaded")
        self.home_page.navbar_horizontal.click_shop_by_category("Beauty and Saloon")
        assert self.page.url == f"{BASE_URL}/"
        
    

