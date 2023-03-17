from flask_restx import Namespace, Resource, fields, reqparse, abort

from server import db
from server.apis.models.treino_model import TreinoModel
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
    'cpf_usuario': fields.String(required=True),
    'nome_exercicio': fields.String(required=True),
    'series': fields.Integer(required=True),
    'repeticoes': fields.Integer(required=True),
    'data_fim': fields.DateTime(required=True),
    'modalidade': fields.Integer(required=True),
    'frequencia': fields.Integer(required=True),
    'carga': fields.Integer(required=True),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'created_by': fields.String,
    'updated_by': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('cpf_usuario')


@treino.route('')
class Treino(Resource):

    @treino.param('cpf_usuario')
    @treino.expect(parser)
    @treino.marshal_with(treino_model_response, 200)
    def get(self):
        params = {key: value for key, value in parser.parse_args().items() if value}
        if params:
            data = db.session.query(TreinoModel).filter_by(**params)
        else:
            data = db.session.query(TreinoModel).one()
        if data:
            return ConverterData.converter_data_json(data=data)
        return {'message': 'Cant find project'}, 404

    @treino.doc('post treino')
    @treino.expect(treino_model)
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
    @treino.expect(treino_model)
    def put(self):
        try:
            db.session.query(TreinoModel).filter(TreinoModel.id == self.api.payload.get('id')). \
                update(self.api.payload, synchronize_session=False)
            db.session.commit()
            return 'update with sucess', 200
        except Exception as exception:
            return exception.args[0], 400
