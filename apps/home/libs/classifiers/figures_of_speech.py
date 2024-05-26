from  apps.home.libs.chat import chats


class figures_of_speech:
    def maritalk_irony_classifier(text):
        prompt = """Classifique o texto por conter Ironia. Responda com a palavra 'sim' se o texto contém ironia ou sarcasmo,
        e responda com a palavra  'nao' caso o texto não contenha ironia ou sarcasmo. Responda apenas com as palavras 'sim' ou 'nao'.

        Texto: Sua beleza é tão linda quanto um pôr do sol na praia.
        Contem_ironia: nao

        Texto: Ótimo dia para o carro estragar!
        Contem_ironia: sim

        Texto: """ + str(text) + """
        Contem_ironia:"""

        answer = chats.basicMaritalk(prompt)

        return answer.strip()