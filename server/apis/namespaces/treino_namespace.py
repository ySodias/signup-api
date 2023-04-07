from flask_restx import Namespace, Resource, fields, reqparse, abort

from server import db
from server.apis.models.treino_model import TreinoModel, ViewTreinoModel
from server.utils.converter_data import ConverterData

treino = Namespace('treino')

treino_model = treino.model('Treino', {
    'cpf_usuario': fields.String(required=True),
    'nome_exercicio': fields.String(required=True),
    'series': fields.Integer(required=True),
    'repeticoes': fields.Integer(required=True),
    'data_fim': fields.String(required=True),
    'modalidade': fields.Integer(required=True),
    'frequencia': fields.Integer(required=True),
    'carga': fields.Integer(required=True)
})

treino_model_response = treino.model('TreinoResponse', {
    'id': fields.Integer(required=True),
    'nome_cliente': fields.String(required=True),
    'nome_exercicio': fields.String(required=True),
    'tipo_exercicio': fields.String(required=True),
    'repeticoes': fields.Integer(required=True),
    'frequencia': fields.Integer(required=True),
    'carga': fields.Integer(required=True),
    'data_inicio': fields.String(required=True),
    'data_troca': fields.String(required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('nome_cliente')


@treino.route('')
class Treino(Resource):

    @treino.param('nome_cliente')
    @treino.expect(parser)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            data = db.session.query(ViewTreinoModel).filter_by(**params).all()
        else:
            data = db.session.query(ViewTreinoModel).one()
        if data:
            return [ConverterData.converter_data_json(data=d) for d in data]
        return {'message': 'Cant find project'}, 404

    @treino.doc('post treino')
    @treino.expect(treino_model, validate=True)
    def post(self):
        treino = TreinoModel()
        for key, value in self.api.payload.items():
            setattr(treino, key, value)
        db.session.add(treino)
        try:
            db.session.commit()
            return 'create with sucess', 201
        except Exception as exception:
            return exception.args[0], 400

    @treino.doc('put treino')
    @treino.expect(treino_model, validate=True)
    def put(self):
        try:
            db.session.query(TreinoModel).filter(TreinoModel.id == self.api.payload.get('id')). \
                update(self.api.payload, synchronize_session=False)
            db.session.commit()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400
