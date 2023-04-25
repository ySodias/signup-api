from flask import g
from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy import desc

from server import db
from server.apis.models.pagamento_model import PagamentoModel, ViewPagamentoMoel
from server.apis.models.usuario_model import UsuarioModel
from server.utils.converter_data import ConverterData

listar_pagamentos = Namespace('listar_pagamentos')
pagamento = Namespace('pagamento')

pagamento_model = pagamento.model('Pagamento', {
    'id': fields.Integer,
    'cpf_usuario': fields.String(required=True),
    'data_vencimento': fields.String(required=True),
    'forma_pagamento': fields.Integer(required=True),
})

pagamento_model_response = pagamento.model('PagamentoResponse', {
    'id': fields.Integer(required=True),
    'cpf_usuario': fields.String(required=True),
    'data_vencimento': fields.String(required=True),
    'forma_pagamento': fields.String(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
    'created_by': fields.String,
    'updated_by': fields.String
})

vw_pagamento_model_response = pagamento.model('VWPagamentoResponse', {
    'id': fields.Integer(required=True),
    'nome': fields.String(required=True),
    'cadastrado_em': fields.String(required=True),
    'status_matricula': fields.String(required=True),
    'vencimento_mensalidade': fields.String(required=True),
    'estado_matricula': fields.Boolean(required=True),
    'ultima_mensalidade_paga': fields.String(required=True),
    'valor': fields.String(required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('cpf_usuario')

ativo_parser = reqparse.RequestParser()
ativo_parser.add_argument('estado_matricula')

@listar_pagamentos.route('')
class Lista_Pagamentos(Resource):

    @listar_pagamentos.doc('get pagamentos')
    @listar_pagamentos.param('estado_matricula')
    @listar_pagamentos.expect(ativo_parser)
    @listar_pagamentos.marshal_list_with(vw_pagamento_model_response)
    def get(self):
        params = {key: value for key, value in ativo_parser.parse_args().items() if value}
        if params:

            list_data = db.session.query(ViewPagamentoMoel).filter_by(**params)
        else:
            list_data = db.session.query(ViewPagamentoMoel).all()
        response = ConverterData.data_to_json_list(list_data)
        return response

@pagamento.route('/usuario')
class Pagamento(Resource):

    @pagamento.param('cpf_usuario')
    @pagamento.expect(parser)
    @pagamento.marshal_with(pagamento_model_response, 200)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            data = db.session.query(PagamentoModel).filter_by(**params).order_by(desc(PagamentoModel.data_vencimento))
        else:
            data = db.session.query(PagamentoModel).all()
        response = ConverterData.converter_data_json(data=data[0])
        return response

    @pagamento.doc('post pagamentos')
    @pagamento.expect(pagamento_model, validate=True)
    def post(self):
        pagamento = PagamentoModel()
        for key, value in self.api.payload.items():
            setattr(pagamento, key, value)
            pagamento.created_by = g.user
        db.session.add(pagamento)
        try:
            db.session.commit()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @pagamento.doc('post pagamentos')
    @pagamento.expect(pagamento_model, validate=True)
    def put(self):
        try:
            db.session.query(PagamentoModel).filter(
                PagamentoModel.id == self.api.payload.get('id')). \
                update(self.api.payload)
            db.session.commit()
            db.session.close()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400