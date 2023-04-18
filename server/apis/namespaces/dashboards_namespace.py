from flask_restx import Namespace, Resource, fields
import requests
from server import environment

dashboards = Namespace('dashboards')

dashboards_model_response = dashboards.model('Dashboards', {
    'token': fields.String(required=True)
})

@dashboards.route('')
class Dashboards(Resource):

    @dashboards.doc('get dashboards')
    @dashboards.marshal_with(dashboards_model_response, 200)
    def post(self):
        url = 'https://login.microsoftonline.com/common/oauth2/token'
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': 'fpc=Ar9JAx08weZOsOREf4rEufI_8lkqAQAAAJws5NkOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
        }
        payload='grant_type=password&scope=openid&resource=https%3A%2F%2Fanalysis.windows.net%2Fpowerbi%2Fapi&client_id=b142d4c6-0f74-4114-87db-875079893e26&username=yuri.soares2%40fatec.sp.gov.br&password=Qxwc1357!'
        response = requests.post(url, headers=headers, data=payload)
        print(response)
        return {'token': response.json().get('access_token')}
