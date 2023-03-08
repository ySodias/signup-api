from server.tests.base_test import BaseTest
from server.tests.integration import BASE_URL

PAYLOAD = {
    "id": 1,
    "taxa_juros": 2.2,
    "dias_vencidos": "2023-03-04 16:51:42.294323"
}


class TestPoliticaPagamento(BaseTest):

    def test_get_politica_pagamento_200(self):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/politica_pagamento', json=PAYLOAD)
                request = client.get(f'{BASE_URL}/politica_pagamento')

                self.assertEqual(request.status_code, 200)

    def test_post_politica_pagamento_201(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                request = client.post(f'{BASE_URL}/politica_pagamento', json=PAYLOAD)

                self.assertEqual(request.status_code, 201)

    def test_put_politica_pagamento_200(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/politica_pagamento', json=PAYLOAD)
                payload = PAYLOAD
                payload['id'] = 1
                payload['taxa_juros'] = 3.0
                request = client.put(f'{BASE_URL}/politica_pagamento', json=payload)

                self.assertEqual(request.status_code, 200)
