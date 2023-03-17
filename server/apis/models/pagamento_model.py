import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey, BigInteger



from server import db
from server.apis.models.dominio_model import DominioModel
from server.apis.models.usuario_model import UsuarioModel


class PagamentoModel(db.Model):
    __tablename__ = 'tb_pagamento'

    id = db.Column(Integer, primary_key=True, nullable=False)
    cpf_usuario = db.Column(String, ForeignKey(UsuarioModel.cpf), nullable=False)
    data_vencimento = db.Column(String, nullable=False)
    forma_pagamento = db.Column(Integer, ForeignKey(DominioModel.id), nullable=False)
    valor_pagamento = db.Column(BigInteger, ForeignKey(DominioModel.id), nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())# data_pagamento
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
