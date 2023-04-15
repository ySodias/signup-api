from flask import g
from flask_restx import Namespace, Resource, fields, reqparse

from server import db
from server.apis.models.administrador_model import AdministradorModel
from server.apis.models.usuario_model import UsuarioModel
from server.utils.converter_data import ConverterData

administrador = Namespace('administrador')


administrador_model = administrador.model('Administrador', {
    'id': fields.Integer,
    'nome': fields.String(required=True),
    'password': fields.String(required=True),
    'email': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'endereco': fields.String(required=True),
    'telefone': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'nivel_permissao': fields.Integer
})

administrador_model_response = administrador.model('AdministradorResponse', {
    'id': fields.Integer,
    'nome': fields.String(required=True),
    'email': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'endereco': fields.String(required=True),
    'telefone': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'nivel_permissao': fields.Integer
})

parser = reqparse.RequestParser()
parser.add_argument('nome')
parser.add_argument('ativo')
parser.add_argument('id')

@administrador.route('')
class Administrador(Resource):

    @administrador.doc('get usuario')
    @administrador.expect(parser)
    @administrador.marshal_with(administrador_model_response, 200)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            usuarios = db.session.query(UsuarioModel).filter_by(**params)
        else:
            usuarios = db.session.query(UsuarioModel).all()
        response = list()
        for usuario in usuarios:
            response.append(ConverterData.converter_data_json(data=usuario).copy())
        return response

    @administrador.doc('post usuario')
    @administrador.expect(administrador_model, validate=True)
    def post(self):
        administrador = AdministradorModel()
        for key, value in self.api.payload.items():
            setattr(administrador, key, value)
        db.session.add(administrador)
        try:
            administrador.created_by = g.user
            db.session.commit()
            db.session.close()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @administrador.doc('put usuario')
    @administrador.expect(administrador_model, validate=True)
    def put(self):
        try:
            db.session.query(AdministradorModel).filter(
                AdministradorModel.id == self.api.payload.get('id')). \
                update(self.api.payload)
            db.session.commit()
            db.session.close()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400
