from flask_restx import Namespace, Resource, fields
from server.core.autenticacao_core import AutenticacaoCore

autenticacao = Namespace('autenticacao')

autenticacao_model = autenticacao.model('Autenticacao', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

autenticacao_model_reponse = autenticacao.model('AutenticacaoResponse', {
    'id': fields.Integer(required=True),
    'nome': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'endereco': fields.String(required=True),
    'telefone': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'token': fields.String(required=True),
})

@autenticacao.route('')
class Autenticacao(Resource):

    @autenticacao.doc('get autenticacao')
    @autenticacao.marshal_with(autenticacao_model_reponse, 200)
    @autenticacao.expect(autenticacao_model)
    def post(self):
        try:
            administrador = AutenticacaoCore.get_administrador_por_usuario(autenticacao_model=self.api.payload)
            if administrador:
                administrador['token'] = AutenticacaoCore.autenticacao(administrador)
            return administrador
        except:
            return None