from playwright.sync_api import sync_playwright

class url_converter:
    
    ##############################################################
    def url_to_html(url):
        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True)

                page = browser.new_page()
                page.goto(url)
                page.wait_for_timeout(10000)  # Aguarda 10 segundos

                html_renderizado = page.content()
                browser.close()

                return html_renderizado
        except Exception as e:
            print(e)
            return False
    ##############################################################
