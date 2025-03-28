from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.google.com')

        page.fill('textarea[name="q"]', 'python')
        page.click('input[type="submit"]')

        page.wait_for_timeout(5000)

        browser.close()

if __name__ == '__main__':
    main()
