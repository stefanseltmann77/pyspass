import flask
import pytest

from pyspass import PySpassRequest


@pytest.fixture()
def flask_app():
    app = flask.Flask(__name__)
    app.testing = True
    return app.test_client()


@pytest.fixture()
def requ():
    return PySpassRequest(flask.request, framework="flask")


class TestPySpassRequest:

    def test_init_for_flask(self):
        requ = PySpassRequest(flask.request, framework="flask")
        assert requ

    def test_init_for_wrong_framework(self):
        with pytest.raises(NotImplementedError):
            PySpassRequest(flask.request, framework="ABC")

    def test_access_to_missing_content(self, flask_app, requ):
        """Empty string, if not in request obj"""
        with flask_app as c:
            c.post("abc=abc")
            assert requ.get("not_there") == ''

    def test_access_to_missing_content_as_int(self, flask_app, requ):
        """None, if not in request obj"""
        with flask_app as c:
            c.post("abc=abc")
            assert requ.get_int("not_there") is None

    def test_access_to_missing_content_as_float(self, flask_app, requ):
        """None, if not in request obj"""
        with flask_app as c:
            c.post("abc=abc")
            assert requ.get_float("not_there") is None
