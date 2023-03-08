from flask_restx import Namespace, Resource

autenticacao = Namespace('autenticacao')

@autenticacao.route('')
class Autenticacao(Resource):

    @autenticacao.doc('get autenticacao')
    def post(self):
        return 'it works'