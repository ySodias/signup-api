import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey

from server import db
from server.apis.models.dominio_model import DominioModel
from server.apis.models.usuario_model import UsuarioModel


class TreinoModel(db.Model):
    __tablename__ = 'tb_treino'

    id = db.Column(Integer, primary_key=True)
    cpf_usuario = db.Column(String, ForeignKey(UsuarioModel.cpf))
    nome_exercicio = db.Column(String)
    series = db.Column(Integer)
    repeticoes = db.Column(Integer)
    data_fim = db.Column(String)
    modalidade = db.Column(Integer, ForeignKey(DominioModel.id))
    frequencia = db.Column(Integer)
    carga = db.Column(Integer)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())# data_inicio
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
