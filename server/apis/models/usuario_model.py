import datetime
from sqlalchemy import DateTime, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server import db
from server.apis.models.dominio_model import DominioModel


class UsuarioModel(db.Model):
    __tablename__ = 'tb_usuario'

    id = db.Column(Integer, primary_key=True)
    cpf = db.Column(String, unique=True, nullable=False)
    nome_cliente = db.Column(String, unique=True, nullable=False)
    data_nascimento = db.Column(String, nullable=False)
    endereco = db.Column(String, nullable=False)
    forma_pagamento = db.Column(Integer, ForeignKey(DominioModel.id), nullable=False)
    telefone = db.Column(String, nullable=False)
    ativo = db.Column(Boolean, nullable=False)
    plano = db.Column(Integer, ForeignKey(DominioModel.id), nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)

