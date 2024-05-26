
from flask_restx import reqparse
from apps.home.models import Empresa
from apps import db
from sqlalchemy import exc, asc, desc
import re
import os 
import json

class empresalib:

    #####################################################################
    def getEmpresaModel():
        empresaModel = reqparse.RequestParser()
        empresaModel.add_argument('cnpj', type=str, help='CNPJ da empresa. ex.: 11111111111111 ou 11.111.111/1111-11"')
        empresaModel.add_argument('nome_razao', type=str, help='Razão social da empresa. Max: 60 caracteres')
        empresaModel.add_argument('nome_fantasia', type=str, help='Nome fantasia da empresa. Max.: 255 caracteres.')
        empresaModel.add_argument('cnae', type=str, help='Número CNAE. 7 caracteres numéricos.')
        return empresaModel
    #####################################################################

    
    #####################################################################
    def getSortModel():
        sortModel = reqparse.RequestParser()
        sortModel.add_argument('limit', type=int, help='Número de resultado por busca. Máximo de 100 por página.')
        sortModel.add_argument('start', type=int, help='Número da página de resultados.')
        sortModel.add_argument('sort', type=str, help='Ordena o resultado pela coluna selecionada. Padrão ascendente.')
        sortModel.add_argument('dir', type=str, help='Define o sentido da ordenação dos resultados. Opções: "asc" e "desc".')
        return sortModel
    #####################################################################

    #####################################################################
    def getUpdateModel():
        updateModel = reqparse.RequestParser()
        updateModel.add_argument('nome_fantasia', type=str, help='Nome fantasia da empresa. Max.: 255 caracteres.')
        updateModel.add_argument('cnae', type=str, help='Número CNAE. 7 caracteres numéricos.')
        return updateModel
    #####################################################################
    

    #####################################################################
    def getEmpresas(data):
        newLimit = data.get('limit')
        newOrderby = data.get('sort')
        newDir = data.get('dir')
        newStart = data.get('start')
        limit = 10
        max_limit = 100
        orderby = Empresa.nome_razao
        offset = 0

        if(newStart):
            offset = int(newStart)

                
        if((newLimit)):
            if(int(newLimit) <= max_limit):
                limit = int(newLimit)

        if(orderby):
            if(newOrderby == 'nome_fantasia'):
                orderby = Empresa.nome_fantasia
            if(newOrderby == 'cnpj'):
                orderby = Empresa.cnpj
            if(newOrderby == 'cnae'):
                orderby = Empresa.cnae

        if(newDir == 'desc'):
            orderby = desc(orderby)
        else:
            orderby = asc(orderby)

        rows = db.session.execute(db.select(Empresa).limit(limit).order_by(orderby).offset(offset)).all()
        empresas = []

        for row in rows:
            empresa = {
                "id": row.Empresa.id,
                "cnpj": row.Empresa.cnpj,
                "nome_razao": row.Empresa.nome_razao,
                "nome_fantasia": row.Empresa.nome_fantasia,
                "cnae": row.Empresa.cnae,
            }
            empresas.append(empresa)
        
        response = {
            "type": "success",
            "message": "connected",
            "empresas": empresas
        }

        return response, 200
    #####################################################################
    


    #####################################################################
    def getEmpresa(id):
        empresa = db.session.execute(db.select(Empresa).filter_by(id = id).order_by(Empresa.nome_razao)).first()
        if(not empresa):
            response = {
                "type": "fail",
                "message": "Id não encontrado.",
            }
            return (response), 404
        empresa = empresa[0]
        response = {
            "type": "success",
            "message": "Empresa encontrada",
            "empresas": [{
                "id": empresa.id,
                "cnpj": empresa.cnpj,
                "nome_razao": empresa.nome_razao,
                "nome_fantasia": empresa.nome_fantasia,
                "cnae": empresa.cnae,
            }]
        }
        return (response), 200
    #####################################################################
    


    #####################################################################
    def postEmpresa(data):
        if ( (not data['cnpj']) or (not data['nome_razao']) or (not data['nome_fantasia']) or (not data['cnae']) ):
            response = {
                "type": "fail",
                "message": "Campos vazios.",
                "info": "Envie um json com os campos 'cnpj', 'nome_razao', 'nome_fantasia' e 'cnae'."
            }
            return response, 400
        
        cnpj = empresalib.validar_cnpj(data['cnpj'])

        if(not cnpj):
            response = {
                "type": "fail",
                "message": "CNPJ inválido.",
            }
            return response, 400

        exist = db.session.execute(db.select(Empresa).where(Empresa.cnpj == cnpj).order_by(Empresa.nome_razao)).all()
        if(exist):
            response = {
                "type": "fail",
                "message": "CNPJ já existe."
            }
            return response, 409
                
        exist = db.session.execute(db.select(Empresa).where(Empresa.nome_razao == data['nome_razao']).order_by(Empresa.nome_razao)).all()
        if(exist):
            response = {
                "type": "fail",
                "message": "Campo nome_razao já existe."
            }
            return response, 409
        
        empresa = Empresa(
            cnpj=cnpj,
            nome_razao=data['nome_razao'],
            nome_fantasia=data['nome_fantasia'],
            cnae=data['cnae']
        )

        try:
            db.session.add(empresa)
            db.session.commit()
            response = {
                "type": "success",
                "message": "Empresa adicionada.",
                "empresa": {
                    "id": empresa.id,
                    "cnpj": empresa.cnpj,
                    "nome_razao": empresa.nome_razao,
                    "nome_fantasia": empresa.nome_fantasia,
                    "cnae": empresa.cnae
                }
            }
            return response, 201
        except exc.SQLAlchemyError as error:
            print("SQLALCHEMYERROR: ", error)
            response = {
                "type": "fail",
                "message": "Erro desconhecido",
                "info": "Tente novamente mais tarde."
            }
            return response, 500 
    #####################################################################

        
    #####################################################################
    def putEmpresa(id, data):
        if ( (not data['nome_fantasia']) and (not data['cnae']) ):
            response = {
                "type": "fail",
                "message": "Campos vazios.",
                "info": "Envie um json com os campos 'nome_fantasia' e 'cnae'."
            }
            return (response), 400
        
        if(data['cnae']):
            if( (not data['cnae'].isnumeric()) or (len(data['cnae']) != 7) ):
                response = {
                    "type": "fail",
                    "message": "CNAE inválido.",
                }
                return (response), 400
        
        empresa = db.session.execute(db.select(Empresa).filter_by(id = id).order_by(Empresa.nome_razao)).first()

        if(not empresa):
            response = {
                "type": "fail",
                "message": "Id não encontrado.",
            }
            return (response), 404
        
        empresa = empresa[0]
        if(data['nome_fantasia']):
            empresa.nome_fantasia = data['nome_fantasia']
        if(data['cnae']):
            empresa.cnae = data['cnae']

        try:
            db.session.add(empresa)
            db.session.commit()
            response = {
                "type": "success",
                "message": "Empresa Atualizada.",
                "empresa": {
                    "id": empresa.id,
                    "cnpj": empresa.cnpj,
                    "nome_razao": empresa.nome_razao,
                    "nome_fantasia": empresa.nome_fantasia,
                    "cnae": empresa.cnae
                }
            }
            return (response), 200
        except exc.SQLAlchemyError as error:
            print("SQLALCHEMYERROR: ", error)
            response = {
                "type": "fail",
                "message": "Erro desconhecido",
                "info": "Tente novamente mais tarde."
            }
            return (response), 500
    #####################################################################        

        
    #####################################################################
    def deleteEmpresaByCnpj(cnpj):
        cnpj = empresalib.validar_cnpj(cnpj)
        if(not cnpj):
                response = {
                    "type": "fail",
                    "message": "CNPJ inválido.",
                    "info": "Forneça um CNPJ apenas com os números em /api/empresa/delete/123456789123"
                }
                return (response), 400
        empresa = db.session.execute(db.select(Empresa).filter_by(cnpj = cnpj).order_by(Empresa.nome_razao)).first()
        if(not empresa):
            response = {
                "type": "fail",
                "message": "CNPJ não encontrado.",
            }
            return (response), 404
        
        empresa = empresa[0]
        try:
            db.session.delete(empresa)
            db.session.commit()
            response = {
                "type": "success",
                "message": "Empresa Deletada.",
                "empresa": {
                    "id": empresa.id,
                    "cnpj": empresa.cnpj,
                    "nome_razao": empresa.nome_razao,
                    "nome_fantasia": empresa.nome_fantasia,
                    "cnae": empresa.cnae
                }
            }
            return (response), 200
        except exc.SQLAlchemyError as error:
            print("SQLALCHEMYERROR: ", error)
            response = {
                "type": "fail",
                "message": "Erro desconhecido",
                "info": "Tente novamente mais tarde."
            }
            return (response), 500
    #####################################################################



    #####################################################################        
    def deleteEmpresaById(id):
        empresa = db.session.execute(db.select(Empresa).filter_by(id = id).order_by(Empresa.nome_razao)).first()
        if(not empresa):
            response = {
                "type": "fail",
                "message": "Id não encontrado.",
            }
            return (response), 404
        
        empresa = empresa[0]   
        try:
            db.session.delete(empresa)
            db.session.commit()
            response = {
                "type": "success",
                "message": "Empresa Deletada.",
                "empresa": {
                    "id": empresa.id,
                    "cnpj": empresa.cnpj,
                    "nome_razao": empresa.nome_razao,
                    "nome_fantasia": empresa.nome_fantasia,
                    "cnae": empresa.cnae
                }
            }
            return (response), 200
        except exc.SQLAlchemyError as error:
            print("SQLALCHEMYERROR: ", error)
            response = {
                "type": "fail",
                "message": "Erro desconhecido",
                "info": "Tente novamente mais tarde."
            }
            return (response), 500
    #####################################################################
        

#####################################################################
    def loadEmpresas(data):
        filename = 'apps/home/data/empresas.json'
        if not os.path.exists(filename):
            response = {
                "type": "fail",
                "message": "Arquivo json com empresas não encontrado.",
            }
            return (response), 404


        with open(filename, 'r') as jsonFile:
            jsonStr = jsonFile.read()
            jsonData = json.loads(jsonStr)
            for empresa in jsonData['empresas']:
                print(empresa['cnpj'])
                empresa = Empresa(
                    cnpj=empresa['cnpj'],
                    nome_razao=empresa['nome'],
                    nome_fantasia=empresa['nome'],
                    cnae=1234567
                )

                try:
                    db.session.add(empresa)
                    db.session.commit()
                    
                except exc.SQLAlchemyError as error:
                    print("SQLALCHEMYERROR: ", error)
                    response = {
                        "type": "fail",
                        "message": "Erro ao salvar empresas no banco.",
                        "info": "Tente novamente mais tarde."
                    }
                    return response, 500 

        response = {
                "type": "success",
                "message": "Itens carregados"
            }
        return (response), 200





    #####################################################################
    def validar_cnpj(cnpj):
        """
        Valida CNPJs, retornando apenas a string de números válida.
    
        # CNPJs errados
        >>> validar_cnpj('abcdefghijklmn')
        False
        >>> validar_cnpj('123')
        False
        >>> validar_cnpj('')
        False
        >>> validar_cnpj(None)
        False
        >>> validar_cnpj('12345678901234')
        False
        >>> validar_cnpj('11222333000100')
        False
    
        # CNPJs corretos
        >>> validar_cnpj('11222333000181')
        '11222333000181'
        >>> validar_cnpj('11.222.333/0001-81')
        '11222333000181'
        >>> validar_cnpj('  11 222 333 0001 81  ')
        '11222333000181'
        """
        cnpj = ''.join(re.findall('\d', str(cnpj)))

        if (not cnpj) or (len(cnpj) < 14):
            return False

        # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
        inteiros = list(map(int, cnpj))
        novo = inteiros[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        # Se o número gerado coincidir com o número original, é válido
        if novo == inteiros:
            return cnpj
        return False
    #####################################################################