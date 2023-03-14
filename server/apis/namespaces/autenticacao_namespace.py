from flask_restx import Namespace, Resource, fields

autenticacao = Namespace('autenticacao')

autenticacao_model = autenticacao.model('Autenticacao', {
    'cpf': fields.String(required=True),
    'senha': fields.String(required=True)
})

autenticacao_model_reponse = autenticacao.model('AutenticacaoResponse', {
    'cpf': fields.String(required=True),
    'nome_cliente': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'endereco': fields.String(required=True),
    'forma_pagamento': fields.Integer(required=True),
    'telefone': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'plano': fields.Integer(required=True),
    'tipo_usuario': fields.Integer(required=True)
})

@autenticacao.route('')
class Autenticacao(Resource):

    @autenticacao.doc('get autenticacao')
    def post(self):
        return 'it works'