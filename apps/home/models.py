from flask_login import UserMixin

from apps import db

class Empresa(db.Model, UserMixin):

    __tablename__ = 'Empresas'

    id            = db.Column(db.Integer, primary_key=True)
    cnpj          = db.Column(db.String(20), unique=True)
    nome_razao    = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(255))
    cnae          = db.Column(db.String(8))
