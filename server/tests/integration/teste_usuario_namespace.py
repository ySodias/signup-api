import mixer as mixer
import pytest as pytest

from server.apis.models.dominio_model import DominioModel
from server.apis.models.usuario_model import UsuarioModel
from server.tests.base_test import BaseTest

BASE_URL = '/v1'

PAYLOAD = {
    "cpf": "999.999.999-99",
    "nome_cliente": "Teste",
    "data_nascimento": "Teste",
    "endereco": "Teste",
    "forma_pagamento": 1,
    "telefone": "Teste",
    "ativo": True,
    "plano": 1,
    "tipo_usuario": 1
    }

@pytest.fixture()
def criar_dominio():
    payload = {
        'nome_dominio': 'teste',
        'tipo_dominio': 'teste'
    }
    yield mixer.blend(DominioModel, **payload)

class TestUsuario(BaseTest):

    def test_get_usuario_200(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                client.post(f'{BASE_URL}/usuario', json=PAYLOAD)
                request = client.get(f'{BASE_URL}/usuario')

                self.assertEqual(request.status_code, 200)

    def test_post_usuario_201(self, *criar_dominio):
        with self.app() as client:
            with self.app_context():
                request = client.post(f'{BASE_URL}/usuario', json=PAYLOAD)

                self.assertEqual(request.status_code, 201)

