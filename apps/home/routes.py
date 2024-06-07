# -*- encoding: utf-8 -*-

from apps.home import blueprint
from apps import api
from flask_restx import Resource
from apps.home.empresas import empresalib
from apps.home.libs.chat import chats
from apps.home.libs.api_models import apiModels
from apps.home.libs.classifiers.figures_of_speech import figures_of_speech
from apps.home.libs.converters.file_to_text import file_to_text



empresaModel = empresalib.getEmpresaModel()
sortModel = empresalib.getSortModel()
updateModel = empresalib.getUpdateModel()
basicOpenaiChat = apiModels.basicOpenaiChat()
basicMaritalkChat = apiModels.basicMaritalkChat()

#################################################################################
@api.route('/api')
class RootApi(Resource):

    #########################################
    @api.doc(description="Teste de coneção.")

    def get(self):
        response = {
            "type": "success",
            "message": "connected",
            "info": "API para cadastro de empresas, construída por Roger Morais Borges para a eStracta."
        }
        return (response)    
    ##########################################

#################################################################################




#####################################################################################
@api.route('/api/empresa')
class EmpresaApi(Resource):
    
    ##########################################    
    @api.doc(parser=sortModel)
    @api.doc(description="Listagem das empresas. Com paginação e ordenação.")
    @api.response(200, 'Sucesso.')

    def get(self):
        data = sortModel.parse_args()
        return empresalib.getEmpresas(data)
    #############################################
    

    ###########################################
    @api.doc(parser=empresaModel)
    @api.doc(description="Salve novas empresas no base de dados. ")
    @api.response(400, 'Campos obrigatórios vazios ou CNPJ inválido.')
    @api.response(409, 'CNPJ ou "nome_razao" já existem.')
    @api.response(201, 'Empresa adicionada com sucesso.')
    @api.response(500, 'Erro interno no servidor.')

    def post(self):
        data = empresaModel.parse_args()
        return empresalib.postEmpresa(data)
    ################################################

##########################################################################################





####################################################################################
@api.route('/api/empresa/cnpj/<string:cnpj>')
class EmpresaCnpj(Resource):
    
    ###########################################
    @api.doc(description="Delete uma empresa pelo CNPJ. Aceita apenas caracteres numéricos. ex.: 11111111111111 ;")
    @api.response(400, 'CNPJ Inválido')
    @api.response(404, 'CNPJ não encontrado')
    @api.response(200, 'Empresa deletada com sucesso.')
    @api.response(200, 'Erro interno no servidor.')

    def delete(self, cnpj):
        return empresalib.deleteEmpresaByCnpj(cnpj)
    ############################################

######################################################################################
        




#########################################################################################
@api.route('/api/empresa/id/<int:id>')
class EmpresaById(Resource):

    #########################################
    @api.response(404, 'Id não encontrado.')
    @api.response(200, 'Empresa Encontrada.')
    @api.doc(description="Lista empresa se houver com o id fornecido.")

    def get(self, id):
        return empresalib.getEmpresa(id)
    #########################################        

    #########################################
    @api.doc(description="Atualiza dados da empresa. Permite atualizar apenas 'nome_fantasia' e 'cnae'. Outros campos serão ignorados.")
    @api.doc(parser=updateModel)
    @api.response(400, 'Campos obrigatórios vazios ou inválidos.')
    @api.response(404, 'Id não encontrado.')
    @api.response(200, 'Empresa atualizada com sucesso.')
    @api.response(500, 'Erro interno no servidor.')

    def put(self, id):
        data = updateModel.parse_args()
        return empresalib.putEmpresa(id, data)
    ###########################################
        
    ############################################
    @api.doc(description="Delete uma empresa através do Id.")
    @api.response(404, 'Id não encontrado.')
    @api.response(200, 'Empresa deletada com sucesso.')
    @api.response(500, 'Erro interno no servidor.')

    def delete(self, id):
        return empresalib.deleteEmpresaById(id)
    ##############################################

#######################################################################################        


#####################################################################################
@api.route('/api/loaddata')
class LoadEmpresaApi(Resource):
    
    ##########################################    
    @api.doc(description="Load de empresas no banco.")
    @api.response(200, 'Sucesso.')

    def get(self):
        data = sortModel.parse_args()
        return empresalib.loadEmpresas(data)
    #############################################
    

##########################################################################################

#####################################################################################
@api.route('/api/basic-chat-openai')
class BasicChatOpenai(Resource):
    
    ##########################################    
    @api.doc(description="Chat Básico com modelo gpt-3.5-turbo-16k")
    @api.doc(parser=basicOpenaiChat)

    @api.response(200, 'Sucesso.')

    def post(self):
        data = basicOpenaiChat.parse_args()
        resposta = chats.basicOpenai(data['user'])
        return resposta, 200
    #############################################
    

##########################################################################################


#####################################################################################
@api.route('/api/basic-chat-maritalk')
class BasicChatMaritalk(Resource):
    
    ##########################################    
    @api.doc(description="Chat Básico com modelo Maritalk")
    @api.doc(parser=basicMaritalkChat)

    @api.response(200, 'Sucesso.')

    def post(self):
        data = basicMaritalkChat.parse_args()
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

    def post(self):
        data = apiModels.docxToText().parse_args()
        resposta = file_to_text.docxToText(data['file'])
        return resposta, 200
    #############################################
    

##########################################################################################