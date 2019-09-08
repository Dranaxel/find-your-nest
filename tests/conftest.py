import pytest, sys

sys.path.append('.')
from FYN import app as FYNapp

@pytest.fixture
def app():
    app = FYNapp 
    return app

@pytest.fixture
def client():
    app = FYNapp
    client = app.test_client()
    yield client
