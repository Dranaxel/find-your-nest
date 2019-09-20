def post(client , add, hh, mn):
    return client.post('/', data=dict(addresse=add, hours=hh, minutes=mn), follow_redirects=True)


def test_main_recherche(client):
    testrecherche = post(client , "69 rue Saint-sabin 75011 Paris", 00, 45)
    assert testrecherche.status_code==200


    
