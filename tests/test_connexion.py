def test_connexion(client):
    response = client.get('/connexion/')
    assert response.status_code == 200
    
def test_connexion2(client):
    
    response = client.post('/connexion/')
    assert response.status_code == 200


