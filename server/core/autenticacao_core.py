import datetime
import re
from functools import wraps
import jwt
from server import db, environment
from server.apis.models.administrador_model import AdministradorModel
from flask import request
from server.utils.converter_data import ConverterData


class AutenticacaoCore:
    @staticmethod
    def get_administrador_por_usuario(autenticacao_model: dict):
        try:
            data = db.session.query(AdministradorModel).filter_by(**autenticacao_model).one()
            response = ConverterData.converter_data_json(data=data)
            return response
        except:
            return None

    @staticmethod
    def autenticacao(administrador):
        administrador['exp'] = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode(administrador, environment.secret_key)
        administrador['exp'] = str(administrador['exp'])
        return token

def token_required():
    token = request.headers.environ.get('HTTP_TOKEN')
    if not token:
        return 'Não autorizado', 401
    try:
        data = jwt.decode(token, environment.secret_key, algorithms=['HS256'])
        del data['exp']
        current_user = AutenticacaoCore.get_administrador_por_usuario(autenticacao_model=data)
    except:
        return 'Não autorizado', 401
    return current_user