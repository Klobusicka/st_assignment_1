from unittest import TestCase
from tunepalapi import TunePalAPI

class TestTunePalAPI(TestCase):
    def setUp(self):
        self.api = TunePalAPI()