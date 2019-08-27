import pytest
import sys

sys.path.append('.')
from FYN import app as FYNapp

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client
