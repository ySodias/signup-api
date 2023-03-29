import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey

from server import db
from server.apis.models.dominio_model import DominioModel
from server.apis.models.usuario_model import UsuarioModel


class TreinoModel(db.Model):
    __tablename__ = 'tb_treino'

    id = db.Column(Integer, primary_key=True)
    cpf_usuario = db.Column(String, ForeignKey(UsuarioModel.cpf), nullable=False)
    nome_exercicio = db.Column(String, nullable=False)
    series = db.Column(Integer, nullable=False)
    repeticoes = db.Column(Integer, nullable=False)
    data_fim = db.Column(String, nullable=False)
    modalidade = db.Column(Integer, ForeignKey(DominioModel.id), nullable=False)
    frequencia = db.Column(Integer, nullable=False)
    carga = db.Column(Integer, nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())# data_inicio
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)

class ViewTreinoModel(db.Model):
    __tablename__ = 'vw_treino'

    id = db.Column(Integer, primary_key=True, nullable=False)
    nome_cliente = db.Column(String)
    nome_exercicio = db.Column(String)
    tipo_exercicio = db.Column(String)
    repeticoes = db.Column(Integer)
    carga = db.Column(String)
    frequencia = db.Column(Integer)
    data_inicio = db.Column(String)
    data_troca = db.Column(String)
