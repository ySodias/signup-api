from flask_restx import Namespace, Resource, fields, reqparse

from server import db
from server.apis.models.politica_pagamento_model import PoliticasPagamentosModel
from server.utils.converter_data import ConverterData

politica_pagamento = Namespace('politica_pagamento')

politica_pagamento_model = politica_pagamento.model('PoliticaPagamento', {
    'id': fields.Integer(required=True),
    'taxa_juros': fields.Integer(required=True),
    'dias_vencidos': fields.String(required=True)
})

politica_pagamento_model_response = politica_pagamento.model('PoliticaPagamentoResponse', {
    'id': fields.Integer(required=True),
    'taxa_juros': fields.Integer(required=True),
    'dias_vencidos': fields.String(required=True),
    'created_at': fields.String,
    'updated_at': fields.String,
    'created_by': fields.String,
    'updated_by': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('taxa_juros')

@politica_pagamento.route('')
class PoliticaPagamento(Resource):

    @politica_pagamento.doc('get politica_pagamento')
    @politica_pagamento.expect(parser)
    @politica_pagamento.marshal_with(politica_pagamento_model_response, 200)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            data = db.session.query(PoliticasPagamentosModel).filter_by(**params)
        else:
            data = db.session.query(PoliticasPagamentosModel).all()
        response = ConverterData.converter_data_json(data=data[0])
        return response


    @politica_pagamento.doc('post politica_pagamento')
    @politica_pagamento.expect(politica_pagamento_model, validate=True)
    @politica_pagamento.marshal_with(politica_pagamento_model_response, 201)
    def post(self):
        politica_pagamento = PoliticasPagamentosModel()
        for key, value in self.api.payload.items():
            setattr(politica_pagamento, key, value)
        db.session.add(politica_pagamento)
        try:
            db.session.commit()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @politica_pagamento.doc('put politica_pagamento')
    @politica_pagamento.expect(politica_pagamento_model, validate=True)
    @politica_pagamento.marshal_with(politica_pagamento_model_response, 200)
    def put(self):
        try:
            db.session.query(PoliticasPagamentosModel).filter(PoliticasPagamentosModel.id == self.api.payload.get('id')). \
                update(self.api.payload, synchronize_session=False)
            db.session.commit()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400