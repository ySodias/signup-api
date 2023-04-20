from flask_restx import Resource

from server.apis.namespaces.administrador_namespace import administrador
from server.apis.namespaces.autenticacao_namespace import autenticacao
from server.apis.namespaces.pagamentos_namespace import pagamento, listar_pagamentos
from server.apis.namespaces.politica_pagamento_namespace import politica_pagamento
from server.apis.namespaces.treino_namespace import treino
from server.apis.namespaces.usuario_namespace import usuario, listar_usuarios
from server import app, api_blueprint, api, environment, db
from server.filter import before_request_func, after_request_func


class Main(Resource):

    def __init__(self):
        app.register_blueprint(api_blueprint)

    def add_namepaces(self):
        api.add_namespace(usuario)
        api.add_namespace(listar_usuarios)
        api.add_namespace(treino)
        api.add_namespace(listar_pagamentos)
        api.add_namespace(pagamento)
        api.add_namespace(politica_pagamento)
        api.add_namespace(autenticacao)
        api.add_namespace(administrador)

    def run(self):
        self.add_namepaces()
        db.init_app(app)
        app.run(port=environment.port, host=environment.host, debug=environment.debug)

if __name__ == '__main__':
    Main().run()

