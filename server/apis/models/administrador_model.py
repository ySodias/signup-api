import datetime
from sqlalchemy import DateTime, Boolean, Integer, String, ForeignKey
from server import db
class AdministradorModel(db.Model):
    __tablename__ = 'tb_administrador'

    id = db.Column(Integer, primary_key=True)
    nome = db.Column(String, unique=True)
    data_nascimento = db.Column(String)
    endereco = db.Column(String)
    telefone = db.Column(String)
    ativo = db.Column(Boolean)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
