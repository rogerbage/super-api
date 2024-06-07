from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

class apiModels:

    #####################################################################
    def basicOpenaiChat():
        modelAPI = reqparse.RequestParser()
        modelAPI.add_argument('system', type=str, help='Comando geral do chat. Define o escopo. Ex: Você é um robô gerador de paroxitonas. Max.: 1024 caracteres')
        modelAPI.add_argument('user', type=str, help='Your prompt, question, requiriment, etc. Max.: 4096 caracteres')
        return modelAPI
    #####################################################################


    #####################################################################
    def basicMaritalkChat():
        model = reqparse.RequestParser()
        model.add_argument('user', type=str, help='Your prompt, question, requiriment, etc. Max.: 4096 caracteres')
        return model
    #####################################################################


    #####################################################################
    def ironyClassifier():
        model = reqparse.RequestParser()
        model.add_argument('phrase', type=str, help='Your phrase to be classified.')
        return model
    #####################################################################


    #####################################################################
    def docxToText():
        model = reqparse.RequestParser()
        model.add_argument('file', type=FileStorage, location='files', required=True, help='Arquivo .docx para ser convertido')
        return model
    #####################################################################


    #####################################################################
    def xlsxToHtml():
        model = reqparse.RequestParser()
        model.add_argument('file', type=FileStorage, location='files', required=True, help='Arquivo .xlsx para ser convertido')
        return model
    #####################################################################


    #####################################################################
    def xlsxToCsv():
        model = reqparse.RequestParser()
        model.add_argument('file', type=FileStorage, location='files', required=True, help='Arquivo .csv para ser convertido')
        return model
    #####################################################################


    #####################################################################
    def pdfToText():
        model = reqparse.RequestParser()
        model.add_argument('file', type=FileStorage, location='files', required=True, help='Arquivo .pdf para ser convertido')
        return model
    #####################################################################

    #####################################################################
    def urlToHtml():
        model = reqparse.RequestParser()
        model.add_argument('url', type=str, required=True, help='URL para ser escaneada')
        return model
    #####################################################################