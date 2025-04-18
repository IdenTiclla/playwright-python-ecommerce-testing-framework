class NavbarHorizontal:
    BLOG_OPTION = "ul.horizontal a[href*='/blog/home']"
    SPECIAL_HOT_OPTION = "ul.horizontal a[href*='route=product/special']"
    HOME_OPTION = "ul.horizontal a[href*='/']"

    
    def __init__(self, page):
        self.page = page

    def click_blog(self):
        self.page.click(self.BLOG_OPTION)

    def click_my_account(self):
        self.page.click("#my_account")
        
    def click_special_hot(self):
        self.page.click(self.SPECIAL_HOT_OPTION)

    def click_home_page(self):
        self.page.click(self.HOME_OPTION)

    def click_megamenu_option(self, option):
        # Primero, hacemos click en el botón Mega Menu y esperamos a que esté visible
        mega_menu = self.page.get_by_role("button", name="Mega Menu")
        mega_menu.hover()
        
        # Esperamos a que el menú se abra y el enlace esté visible
        option_link = self.page.get_by_role("link", name=option, exact=True)        
        # Ahora hacemos click en la opción
        option_link.click()

    def click_my_account_option(self, option):
        my_account_option = self.page.get_by_role("button", name=" My account")
        my_account_option.hover()
        option_link = self.page.get_by_role("link", name=option, exact=True)
        option_link.click()