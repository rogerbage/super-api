# -*- encoding: utf-8 -*-

from apps.home import blueprint
from apps import api
from flask_restx import Resource
from apps.home.libs.chat import chats
from apps.home.libs.api_models import apiModels
from apps.home.libs.classifiers.figures_of_speech import figures_of_speech
from apps.home.libs.converters.file_to_text import file_to_text
from apps.home.libs.converters.url_converter import url_converter
from apps.home.libs.converters.db_converter import db_converter



#################################################################################
@api.route('/api')
class RootApi(Resource):

    #########################################
    @api.doc(description="Teste de coneção.")

    def get(self):
        response = {
            "type": "success",
            "message": "connected",
            "info": "API de ferramentas para PLN"
        }
        return (response)    
    ##########################################

#################################################################################
          


#####################################################################################
@api.route('/api/basic-chat-openai')
class BasicChatOpenai(Resource):
    
    ##########################################    
    @api.doc(description="Chat Básico com modelo gpt-3.5-turbo-16k")
    @api.doc(parser=apiModels.basicOpenaiChat())

    @api.response(200, 'Sucesso.')

    def post(self):
        data = apiModels.basicOpenaiChat().parse_args()
        resposta = chats.basicOpenai(data['user'])
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/basic-chat-maritalk')
class BasicChatMaritalk(Resource):
    
    ##########################################    
    @api.doc(description="Chat Básico com modelo Maritalk")
    @api.doc(parser=apiModels.basicMaritalkChat())

    @api.response(200, 'Sucesso.')

    def post(self):
        data = apiModels.basicMaritalkChat().parse_args()
        resposta = chats.basicMaritalk(data['user'])
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/maritalk-irony-classifier')
class MaritalkIronyClassifier(Resource):
    
    ##########################################    
    @api.doc(description="Classificador de ironias usando o modelo LLM Maritalk. Entrada: texto a ser classificado. Saida: 'sim' para ironia e 'nao' para não ironias.")
    @api.doc(parser=apiModels.ironyClassifier())

    @api.response(200, 'Sucesso.')

    def post(self):
        data = apiModels.ironyClassifier().parse_args()
        resposta = figures_of_speech.maritalk_irony_classifier(data['phrase'])
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/docx-to-text')
class DocxToText(Resource):
    
    ##########################################    
    @api.doc(description="Converte um documento docx para texto puro.")
    @api.doc(parser=apiModels.docxToText())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Error converting or not docx')

    def post(self):
        data = apiModels.docxToText().parse_args()
        resposta = file_to_text.docxToText(data['file'])
        if (not resposta):
            return "not docx", 400
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/xlsx-to-html')
class XlsxToHtml(Resource):
    
    ##########################################    
    @api.doc(description="Converte um documento xlsx (Excel) para texto no formato HTML.")
    @api.doc(parser=apiModels.xlsxToHtml())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Error converting or not xlsx')

    def post(self):
        data = apiModels.xlsxToHtml().parse_args()
        resposta = file_to_text.xlsxToHtml(data['file'])
        if (not resposta):
            return "not xlsx", 400
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/pdf-to-text')
class PdfToText(Resource):
    
    ##########################################    
    @api.doc(description="Converte um documento PDF para texto puro.")
    @api.doc(parser=apiModels.pdfToText())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Error converting or not PDF')

    def post(self):
        data = apiModels.pdfToText().parse_args()
        resposta = file_to_text.pdfToText(data['file'])
        if (not resposta):
            return "not PDF", 400
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/url-to-html')
class PdfToText(Resource):
    
    ##########################################    
    @api.doc(description="Retorna o HTML renderizado de uma página Web.")
    @api.doc(parser=apiModels.urlToHtml())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Erro ao capturar HTML')

    def post(self):
        data = apiModels.urlToHtml().parse_args()
        resposta = url_converter.url_to_html(data['url'])
        if (not resposta):
            return "Erro ao capturar HTML", 400
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/chat-db')
class chat_db(Resource):
    
    ##########################################    
    @api.doc(description="Retorna uma tabela HTML com o resultado da consulta.")
    @api.doc(parser=apiModels.chatDb())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Erro ao consultar banco')

    def post(self):
        data = apiModels.chatDb().parse_args()
        resposta = db_converter.chat_db(data)
        if (not resposta):
            return "Erro ao consultar banco", 400
        return resposta, 200
    #############################################
    

##########################################################################################



#####################################################################################
@api.route('/api/db-to-json')
class db_to_json(Resource):
    
    ##########################################    
    @api.doc(description="Retorna um JSON com os principais metadados da um banco de dados.")
    @api.doc(parser=apiModels.dbToJson())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Erro ao consultar banco')

    def post(self):
        data = apiModels.dbToJson().parse_args()
        
        config = {
            'user': data['user'],
            'password': data['password'],
            'host': data['host'],
            'port': data['port'],
            'database': data['database'],
            'raise_on_warnings': True
        }
        
        conn = db_converter.connect_to_mysql(config, attempts=1)

        dbString = False

        if (conn['status'] == 'success'):
            dbString = db_converter.db_to_json(conn['connection'], config['database'])
        
        if (not dbString):
            return "Erro ao consultar banco", 400
        return dbString, 200
    #############################################
    

##########################################################################################



#####################################################################################
@api.route('/api/file-to-text')
class convert_file_to_text(Resource):
    
    ##########################################    
    @api.doc(description="Converte um documento em texto puro. Aceita docx, xlsx e pdf. (xlsx  é convertido para html)")
    @api.doc(parser=apiModels.fileToText())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Error accessing the file')

    def post(self):
        data = apiModels.fileToText().parse_args()

        resposta = file_to_text.fileToText(data['file'])
        if (not resposta):
            return "Error accessing the file", 400
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/chat-file')
class chat_file(Resource):
    
    ##########################################    
    @api.doc(description="Consulta um documento através de linguagem humana. Aceita docx, pdf, xlsx, json, html, xml e csv)")
    @api.doc(parser=apiModels.chatFile())

    @api.response(200, 'Sucesso.')
    @api.response(400, 'Error accessing the file')

    def post(self):
        data = apiModels.chatFile().parse_args()
        resposta = file_to_text.chatFile(data)
        if (not resposta):
            return "Invalid or empty file", 400

        return resposta, 200
    #############################################
    

##########################################################################################