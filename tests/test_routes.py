import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'ok'

def test_data_endpoint(client):
    response = client.get('/api/v1/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_invalid_route(client):
    response = client.get('/invalid')
    assert response.status_code == 404
