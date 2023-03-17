import re

from flask import request

from server import app
from server.core.autenticacao_core import token_required

ALLOWED_URLS = [
    '/v1/autenticacao',
    '/v1/',
    '/swaggerui/droid-sans.css',
    '/swaggerui/swagger-ui.css',
    '/v1/swagger.json',
    '/swaggerui/swagger-ui-bundle.js',
    '/swaggerui/swagger-ui-standalone-preset.js',
    '/swaggerui/favicon-32x32.png',
    '/swaggerui/favicon-16x16.png'
    '/favicon.ico'
]

def validate_form_input(func):
    def wrapper_func():
        if request.content_type == 'application/json':
            REGEX_CPF = re.compile("[0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2}")
            REGEX_DATA = re.compile("[0-9]{4}[-](?:[0][1-9]|[1][0-2])[-](?:[0-2][0-9]|[3][0-1])")
            REGEX_TELEFONE = re.compile("^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$")
            for key, value in request.json.items():
                if 'cpf' in key and re.match(REGEX_CPF, value) is None:
                    return 'Invalid Input', 400
                if isinstance(value, str) and len(value) < 3:
                    return 'Invalid Input', 400
                if 'telefone' in key and re.match(REGEX_TELEFONE, value) is None:
                    return 'Invalid Input', 400
                if ('data' in key or 'dias' in key) and re.match(REGEX_DATA, value) is None:
                    return 'Invalid Input', 400
                if 'email' in key and '@' in value:
                    return 'Invalid Input', 400
    return wrapper_func

@app.before_request
@validate_form_input
def before_request_func():
    usuario_logado = token_required()
    path = request.path
    if isinstance(usuario_logado, tuple) and path not in ALLOWED_URLS:
        return 'Não autorizado', 401


@app.after_request
def after_request_func(response):
    return response

