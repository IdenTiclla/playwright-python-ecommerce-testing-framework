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