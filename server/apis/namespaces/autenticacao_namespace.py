from flask_restx import Namespace, Resource, fields, abort
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
    'nivel_permissao': fields.Integer(required=True),
    'token': fields.String(required=True),
})

autenticacao_model_reponse_error = autenticacao.model('AutenticacaoResponseError', {
    'message': fields.String(required=True),
})

@autenticacao.route('')
class Autenticacao(Resource):

    @autenticacao.doc('get autenticacao')
    @autenticacao.expect(autenticacao_model, validate=True)
    def post(self):
        try:
            administrador = AutenticacaoCore.get_administrador_por_usuario(autenticacao_model=self.api.payload)
            if administrador:
                administrador['token'] = AutenticacaoCore.autenticacao(administrador)
                return administrador, 200
            return '', 404
        except:
            return abort(400, custom='value')