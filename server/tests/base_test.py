from unittest import TestCase

from server import app, db
from server.main import Main


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():
            main = Main()
            main.add_namepaces()
            db.init_app(app)
    def setUp(self):
        # Make sure database exists

        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
