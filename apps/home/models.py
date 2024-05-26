# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Empresa(db.Model, UserMixin):

    __tablename__ = 'Empresas'

    id            = db.Column(db.Integer, primary_key=True)
    cnpj          = db.Column(db.String(20), unique=True)
    nome_razao    = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(255))
    cnae          = db.Column(db.String(8))
