import datetime
from sqlalchemy import DateTime, Boolean, Integer, String
from server import db
class AdministradorModel(db.Model):
    __tablename__ = 'tb_administrador'

    id = db.Column(Integer, primary_key=True, nullable=False)
    email = db.Column(String, unique=True, nullable=False)
    nome = db.Column(String, nullable=False)
    password = db.Column(String, nullable=False)
    data_nascimento = db.Column(String, nullable=False)
    endereco = db.Column(String, nullable=False)
    telefone = db.Column(String, nullable=False)
    ativo = db.Column(Boolean, nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
