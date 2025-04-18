
import pytest
# from pages.auth.login_page import LoginPage
from pages.home_page import HomePage

def test_login(page):
    home = HomePage(page)
    home.goto()
    home.navbar_horizontal.click_my_account_option("Login")
    assert page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"

    # assert that the url contains "account/login"
    assert "account/login" in page.url

    # wait for load state
    page.wait_for_load_state("domcontentloaded")

    home.navbar_horizontal.click_my_account_option("Register")
    assert page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"

    # assert that the url contains "account/register"
    assert "account/register" in page.url

    # wait for load state
    page.wait_for_load_state("domcontentloaded")



