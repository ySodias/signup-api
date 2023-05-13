import os

class Environment:

    def __init__(self):
        self._ENV_API_NAME = os.getenv('API_NAME')

        self._ENV_PORT = os.getenv('PORT') or '8080'
        self._ENV_HOST = os.getenv('HOST') or 'localhost'
        self._ENV_DEBUG = os.getenv('DEBUG') or False
        self._ENV_DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')

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
