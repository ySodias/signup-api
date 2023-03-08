import datetime

from sqlalchemy import DateTime, Integer, String, BigInteger

from server import db


class PoliticasPagamentosModel(db.Model):
    __tablename__ = 'tb_politicas_pagamentos'

    id = db.Column(Integer, primary_key=True)
    taxa_juros = db.Column(BigInteger)
    dias_vencidos = db.Column(String)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(String)
    updated_by = db.Column(String)
