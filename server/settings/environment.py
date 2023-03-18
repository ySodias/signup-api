import os

class Environment:

    def __init__(self):
        self._ENV_API_NAME = os.getenv('API_NAME')

        self._ENV_PORT = os.getenv('PORT') or '8080'
        self._ENV_HOST = os.getenv('HOST') or 'localhost'
        self._ENV_DEBUG = os.getenv('DEBUG') or False
        self._ENV_DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
        self._ENV_SECRET = os.getenv('SECRET')
        self._MICROSOFT_URL = os.getenv('MICROSOFT_URL')
        self._AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
        self._AZURE_USERNAME = os.getenv('AZURE_USERNAME')
        self._AZURE_PASSWORD = os.getenv('AZURE_PASSWORD')
        self._COOKIE = os.getenv('COOKIE')
        self._SECRET_KEY = os.getenv('SECRET_KEY')

    @property
    def api_name(self) -> str:
        return self._ENV_API_NAME

    @property
    def port(self) -> str:
        return self._ENV_PORT

    @property
    def host(self) -> str:
        return self._ENV_HOST

    @property
    def debug(self) -> bool:
        return self._ENV_DEBUG

    @property
    def database_connection(self) -> str:
        return self._ENV_DATABASE_CONNECTION

    @property
    def secret(self) -> str:
        return self._ENV_SECRET
    @property
    def microsoft_url(self) -> str:
        return self._MICROSOFT_URL
    @property
    def secret(self) -> str:
        return self._ENV_SECRET
    @property
    def azure_client_id(self) -> str:
        return self._AZURE_CLIENT_ID
    @property
    def azure_username(self) -> str:
        return self._AZURE_USERNAME
    @property
    def azure_password(self) -> str:
        return self._AZURE_PASSWORD
    @property
    def cookie(self) -> str:
        return self._COOKIE

    @property
    def secret_key(self) -> str:
        return self._SECRET_KEY