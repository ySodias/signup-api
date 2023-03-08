import pytest
from mixer.auto import mixer

from server.apis.models.dominio_model import DominioModel
from server.tests.base_test import BaseTest
from server.tests.integration import BASE_URL

PAYLOAD = {
    'cpf_usuario': "999.999.999-99",
    'nome_exercicio': 'Teste',
    'series': 5,
    'repeticoes': 5,
    'data_fim': '2023-03-04 16:51:42.294323',
    'modalidade': 1,
    'frequencia': 5,
    'carga': 5
}

@pytest.fixture()
def criar_dominio():
    payload = {
        'nome_dominio': 'teste',
        'tipo_dominio': 'teste'
    }
    yield mixer.blend(DominioModel, **payload)

class TestTreino(BaseTest):

    def test_get_treino_200(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/treino', json=PAYLOAD)
                request = client.get(f'{BASE_URL}/treino')

                self.assertEqual(request.status_code, 200)

    def test_post_treino_201(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                request = client.post(f'{BASE_URL}/treino', json=PAYLOAD)

                self.assertEqual(request.status_code, 201)

    def test_put_treino_200(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/treino', json=PAYLOAD)
                payload = PAYLOAD
                payload['id'] = 1
                payload['nome_exercicio'] = 'Teste Put'
                request = client.put(f'{BASE_URL}/treino', json=payload)

                self.assertEqual(request.status_code, 200)
