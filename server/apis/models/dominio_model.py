import datetime
from sqlalchemy import DateTime, Integer, String

from server import db


class DominioModel(db.Model):
    __tablename__ = 'tb_dominio'

    id = db.Column(Integer, primary_key=True, nullable=False)
    nome_dominio = db.Column(String, unique=True, nullable=False)
    tipo_dominio = db.Column(String, nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
