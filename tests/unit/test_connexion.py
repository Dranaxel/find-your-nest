def test_connexion(client):
    response = client.get('/connexion/')
    assert response.status_code == 200

#def connexion(client, email, password):
#    return client.post('/connexion/', data=dict(
#        email = email,
#        password = password))

#def test_connexion2(client):
#    response = connexion(client, email, password)
#    assert response.status_code == 302 

