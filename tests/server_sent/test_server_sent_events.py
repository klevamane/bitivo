""" test server sent functionality """
from flask_sse import sse
from unittest.mock import Mock, patch
import unittest
from manage import app
import flask


class TestServerSentEvent(unittest.TestCase):
    """"Test sever sent events"""
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_testing_server_sucess(self):
        """test server sent publish"""
        sse.publish = Mock()
        res = self.tester.get('/testing_server')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b'Message sent!')

    def test_server_sent_client_sucess(self):
        """ test server sent client """
        res = self.tester.get('/server_sent_client')
        self.assertEqual(res.status_code, 200)
