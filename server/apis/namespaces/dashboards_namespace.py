from flask_restx import Namespace, Resource, fields
from flask import request

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
        url = environment.microsoft_url
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': environment.cookie
        }
        payload=f'grant_type=password&scope=openid&' \
                f'resource=https%3A%2F%2Fanalysis.windows.net%2Fpowerbi%' \
                f'2Fapi&client_id={environment.azure_client_id}&' \
                f'username={environment.azure_username}r&password={environment.azure_password}'
        response = request("POST", url, headers=headers, data=payload)
        return response.json().get('access_token')
