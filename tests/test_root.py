
def test_root(client):
    assert client.get('/').status_code == 200
