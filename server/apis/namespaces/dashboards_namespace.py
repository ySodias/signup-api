from flask_restx import Namespace, Resource

dashboards = Namespace('dashboards')

@dashboards.route('')
class Dashboards(Resource):

    @dashboards.doc('get dashboards')
    def get(self):
        return 'it works'