from src import controller
import pytest
from io import BytesIO

@pytest.fixture
def client():
    with controller.app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    
    assert response.status_code == 200
    
def test_404_error(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404

def test_500_error(client):
    response = client.get('/book/invaliduuid')
    assert response.status_code == 500
