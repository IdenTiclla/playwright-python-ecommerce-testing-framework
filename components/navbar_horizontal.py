class NavbarHorizontal:
    BLOG_OPTION = "ul.horizontal a[href*='/blog/home']"
    def __init__(self, page):
        self.page = page

    def click_blog(self):
        self.page.click(self.BLOG_OPTION)

    def click_my_account(self):
        self.page.click("#my_account")
        
        