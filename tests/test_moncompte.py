
def test_moncompte1(client):
    response =  client.get('/moncompte/')
    assert response.status_code == 200


def test_moncompte2(client):
    response = client.post('/moncompte/')
    assert response.status_code == 200
