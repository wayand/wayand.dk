import unittest
from app import create_app
import config

class BaseTestCase(unittest.TestCase):
    config = config.TestingConfig

    def setUp(self):
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()