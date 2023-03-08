from flask_restx import Namespace, Resource, fields, reqparse

from server import db
from server.apis.models.pagamento_model import PagamentoModel
from server.utils.converter_data import ConverterData

listar_pagamentos = Namespace('listar_pagamentos')
pagamento = Namespace('pagamento')

pagamento_model = pagamento.model('Pagamento', {
    'id': fields.Integer(required=True),
    'cpf_usuario': fields.String(required=True),
    'data_vencimento': fields.String(required=True),
    'forma_pagamento': fields.Integer(required=True),
    'valor_pagamento': fields.Integer(required=True)
})

pagamento_model_response = pagamento.model('PagamentoResponse', {
    'id': fields.Integer(required=True),
    'cpf_usuario': fields.String(required=True),
    'data_vencimento': fields.String(required=True),
    'forma_pagamento': fields.String(required=True),
    'valor_pagamento': fields.String(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
    'created_by': fields.String,
    'updated_by': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('cpf_usuario')

@listar_pagamentos.route('')
class Lista_Pagamentos(Resource):

    @listar_pagamentos.doc('get pagamentos')
    @listar_pagamentos.marshal_with(pagamento_model_response, code=200, as_list=True)
    def get(self):
        list_data = db.session.query(PagamentoModel).all()
        response = ConverterData.paginate_json(list_data)
        return response

@pagamento.route('/usuario')
class Pagamento(Resource):

    @pagamento.param('cpf_usuario')
    @pagamento.expect(parser)
    @pagamento.marshal_with(pagamento_model_response, 200)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            data = db.session.query(PagamentoModel).filter_by(**params)
        else:
            data = db.session.query(PagamentoModel).all()
        response = ConverterData.converter_data_json(data=data[0])
        return response

    @pagamento.doc('post pagamentos')
    @pagamento.expect(pagamento_model)
    @pagamento.marshal_with(pagamento_model_response, 201)
    def post(self):
        pagamento = PagamentoModel()
        for key, value in self.api.payload.items():
            setattr(pagamento, key, value)
        db.session.add(pagamento)
        try:
            db.session.commit()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @pagamento.doc('post pagamentos')
    @pagamento.expect(pagamento_model)
    @pagamento.marshal_with(pagamento_model_response, 200)
    def put(self):
        try:
            db.session.query(PagamentoModel).filter(
                PagamentoModel.id == self.api.payload.get('id')). \
                update(self.api.payload, synchronize_session=False)
            db.session.commit()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400