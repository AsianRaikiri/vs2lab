"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestTelephoneService(unittest.TestCase):
    """The test"""
    
    telephoneDatabase = {
        "Adam": "234723",
        "Levine": "976543234"
    }
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.telephoneBook, args=(telephoneDatabase,))  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_telephone_get(self):  # each test_* function is a test
        """Test simple call"""
        msg = self.client.get("Adam")
        self.assertEqual(msg, "234723")

    def test_telephone_getAll(self): 
        msg = self.client.getAll()
        self.assertEqual(msg,"Adam: 234723, Levine: 976543234")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate

if __name__ == '__main__':
    unittest.main()