from playwright.sync_api import sync_playwright
from apps.home.libs.chat import chats
from apps.home.libs.converters.file_to_text import file_to_text
class url_converter:
    
    ##############################################################
    def url_to_html(url):
        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True)

                page = browser.new_page()
                page.goto(url)
                page.wait_for_timeout(10000) 

                html_renderizado = page.content()
                browser.close()

                return html_renderizado
        except Exception as e:
            print(e)
            return False
    ##############################################################


    ##############################################################
    def chatUrl(data):
        html = url_converter.url_to_html(data['url'])
        full_prompt = (
            f"Aplique o 'Prompt' no 'HTML' abaixo:\n"
            f"\n###########\n"
            f"Prompt: {data['prompt']}"
            f"\n###########\n"
            f"\n##########\n"
            f"HTML: \n"
            f"{html}"
            f"\n#########\n"
        )

        slices = file_to_text.slice_string(full_prompt, 8000)
        resposta = chats.modeloConcatenaResposta(slices, data['prompt'])
        return resposta

    ##############################################################
