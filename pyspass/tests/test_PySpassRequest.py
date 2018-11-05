import unittest
from unittest import TestCase
import flask
from pyspass import PySpassRequest


class TestPySpassRequest(TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        app.testing = True
        self.app = app.test_client()
        self.request = PySpassRequest(flask.request, framework="flask")

    def test_init_for_flask(self):
        self.request = PySpassRequest(flask.request, framework="flask")

    def test_init_for_wrong_framework(self):
        with self.assertRaises(NotImplementedError):
            PySpassRequest(flask.request, framework="ABC")

    def test_access_to_missing_content(self):
        """Empty string, if not in request obj"""
        with self.app as c:
            c.post("abc=abc")
            self.assertEqual(self.request.get("not_there"), '')

    def test_access_to_missing_content_as_int(self):
        """None, if not in request obj"""
        with self.app as c:
            c.post("abc=abc")
            self.assertEqual(self.request.get_int("not_there"), None)

    def test_access_to_missing_content_as_float(self):
        """None, if not in request obj"""
        with self.app as c:
            c.post("abc=abc")
            self.assertEqual(self.request.get_float("not_there"), None)


if __name__ == '__main__':
    unittest.main()
