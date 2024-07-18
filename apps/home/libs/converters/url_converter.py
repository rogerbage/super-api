from playwright.sync_api import sync_playwright
from apps.home.libs.chat import chats
from apps.home.libs.converters.file_to_text import file_to_text
from bs4 import BeautifulSoup, Comment
import re
from collections import Counter
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
        # print(html)
        # full_prompt = (
        #     f"Aplique o 'Prompt' no 'HTML' abaixo:\n"
        #     f"\n###########\n"
        #     f"Prompt: {data['prompt']}"
        #     f"\n###########\n"
        #     f"\n##########\n"
        #     f"HTML: \n"
        #     f"{html}"
        #     f"\n#########\n"
        # )

        clean_html = url_converter.clean_html(html)

        # print(clean_html)

        slices = file_to_text.slice_string(clean_html, 16000)
        # print(slices)
        resposta = chats.modeloRefinaResposta(slices, data['prompt'] )
        return resposta

    ##############################################################


    ##############################################################
    def clean_html(html):
        soup = BeautifulSoup(html, "html.parser")

        if soup.head:
            soup.head.decompose()
        
        for style in soup.find_all("style"):
            style.decompose()
        
        for script in soup.find_all("script"):
            script.decompose()
        
        for svg in soup.find_all("svg"):
            svg.decompose()

        for div in soup.find_all("div"):
            if not div.get_text(strip=True):
                div.decompose()
            else:
                for attribute in ["id", "class", "style"]:
                    if attribute in div.attrs:
                        del div.attrs[attribute]

        for element in soup.find_all(True):
            element.attrs = {}

        for div in soup.find_all("div"):
            text = div.get_text(strip=True)
            if not text or text.isspace():
                div.decompose()
        
        strings = []

        for element in soup.find_all(text=True):
            if isinstance(element, str):
                strings.append(element.string)
                # print(element.string)
                # if(url_converter.has_repeated_content(element.string, 70)):
                #     element.string = ""

        # for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        #     comment.extract()
        
        return '\n'.join(strings)
    ##############################################################


    def normalize_spaces(text):
        return re.sub(r'\s+', ' ', text)
    

    def has_repeated_content(string, percent):
        if len(string) == 0:
            return False
        
        # Conta a frequência de cada caractere na string
        count = Counter(string)
        
        # Encontra o caractere mais frequente
        mais_frequente = max(count.values())
        
        # Calcula o percentual deste caractere mais frequente em relação ao tamanho da string
        percentual = (mais_frequente / len(string)) * 100
        
        # Verifica se o percentual é igual ou maior que 70
        if percentual >= percent:
            return True
        else:
            return False