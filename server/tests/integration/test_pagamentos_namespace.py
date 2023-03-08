import pytest
from mixer.auto import mixer

from server.apis.models.dominio_model import DominioModel
from server.tests.base_test import BaseTest
from server.tests.integration import BASE_URL

PAYLOAD = {
    'cpf_usuario': '999.999.999-99',
    'data_vencimento': 1,
    'forma_pagamento': 1,
    'valor_pagamento': 1
}


@pytest.fixture()
def criar_dominio():
    payload = {
        'nome_dominio': 'teste',
        'tipo_dominio': 'teste'
    }
    yield mixer.blend(DominioModel, **payload)

class TestPagamento(BaseTest):

    def test_get_pagamento_200(self):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/pagamento/usuario', json=PAYLOAD)
                request = client.get(f'{BASE_URL}/pagamento/usuario')

                self.assertEqual(request.status_code, 200)

    def test_post_pagamento_201(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                request = client.post(f'{BASE_URL}/pagamento/usuario', json=PAYLOAD)

                self.assertEqual(request.status_code, 201)

    def test_put_pagamento_200(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/pagamento/usuario', json=PAYLOAD)
                payload = PAYLOAD
                payload['id'] = 1
                payload['forma_pagamento'] = 2
                request = client.put(f'{BASE_URL}/pagamento/usuario', json=payload)

                self.assertEqual(request.status_code, 200)
