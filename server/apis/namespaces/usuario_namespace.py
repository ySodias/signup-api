from flask_restx import Namespace, Resource, fields, reqparse

from server import db
from server.apis.models.usuario_model import UsuarioModel
from server.core import autenticacao_core
from server.utils.converter_data import ConverterData

usuario = Namespace('usuario')
listar_usuarios = Namespace('listar_usuarios')

usuario_model = usuario.model('Usuario', {
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

usuario_model_response = usuario.model('UsuarioResponse', {
    'id': fields.Integer,
    'cpf': fields.String(required=True),
    'nome_cliente': fields.String(required=True),
    'data_nascimento': fields.String(required=True),
    'endereco': fields.String(required=True),
    'forma_pagamento': fields.Integer(required=True),
    'telefone': fields.String(required=True),
    'ativo': fields.Boolean(required=True),
    'plano': fields.Integer(required=True),
    'tipo_usuario': fields.Integer(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
    'created_by': fields.String,
    'updated_by': fields.String
})


parser = reqparse.RequestParser()
parser.add_argument('nome_cliente')
parser.add_argument('cpf')
parser.add_argument('ativo')

@listar_usuarios.route('')
class Listar_Usuarios(Resource):

    @listar_usuarios.doc('get listar_usuarios')
    @usuario.marshal_with(usuario_model_response, code=200, as_list=True)
    def get(self):
        list_data = db.session.query(UsuarioModel).all()
        response = ConverterData.paginate_json(list_data)
        return response

@usuario.route('')
class Usuario(Resource):

    @usuario.doc('get usuario')
    @usuario.expect(parser)
    @usuario.marshal_with(usuario_model_response, 200)
    def get(self):
        """Params:
        Nome, Estado Matrícula, CPF
        """
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            usuarios = db.session.query(UsuarioModel).filter_by(**params)
        else:
            usuarios = db.session.query(UsuarioModel).all()
        response = list()
        for usuario in usuarios:
            response.append(ConverterData.converter_data_json(data=usuario).copy())
        return response

    @usuario.doc('post usuario')
    @usuario.expect(usuario_model)
    @usuario.marshal_with(usuario_model_response, 201)
    def post(self):
        usuario = UsuarioModel()
        for key, value in self.api.payload.items():
            setattr(usuario, key, value)
        db.session.add(usuario)
        try:
            db.session.commit()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @usuario.doc('put usuario')
    @usuario.expect(usuario_model)
    @usuario.marshal_with(usuario_model_response, 200)
    def put(self):
        try:
            db.session.query(UsuarioModel).filter(UsuarioModel.id == self.api.payload.get('id')).\
            update(self.api.payload, synchronize_session=False)
            db.session.commit()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400

    @usuario.doc('delete usuario')
    @usuario.expect(usuario_model)
    @usuario.marshal_with(usuario_model_response, 200)
    def delete(self):
        """
        Endpoint para delete lógico do usuário
        :return:
        """
        try:
            db.session.query(UsuarioModel).\
                filter(UsuarioModel.nome_cliente == self.api.payload.get('nome_cliente')). \
                update({'ativo': False}, synchronize_session=False)
            db.session.commit()
            return 'delete with sucess', 200
        except Exception as exception:
            return exception.args[0], 400
