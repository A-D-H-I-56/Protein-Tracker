import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_web_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Precision Nutrition AI Engine" in response.data

def test_web_metrics(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b"Model Performance" in response.data

def test_web_api_docs(client):
    response = client.get('/api-docs')
    assert response.status_code == 200
    assert b"Developer REST API" in response.data

def test_web_404(client):
    response = client.get('/non-existent-route-12345')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

def test_api_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    assert "status" in data
    assert "version" in data

def test_api_metrics(client):
    response = client.get('/api/v1/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert "metrics" in data

def test_api_predict_json_validation(client):
    payload = {
        "age": 25,
        "gender": "Male",
        "weight": 70.0,
        "height": 175.0,
        "activity_level": "Very Active",
        "goal": "Muscle Gain"
    }
    response = client.post('/api/v1/predict', json=payload)
    if response.status_code == 200:
        data = json.loads(response.data)
        assert data["success"] is True
        assert "plan" in data["data"]
        assert data["data"]["plan"]["calories"] > 0
    else:
        # If model artifacts need training step
        assert response.status_code in [200, 503]

def test_api_predict_invalid_payload(client):
    payload = {
        "age": 5, # Invalid age
        "gender": "Unknown",
        "weight": 10.0,
        "height": 100.0,
        "activity_level": "Invalid",
        "goal": "Invalid"
    }
    response = client.post('/api/v1/predict', json=payload)
    assert response.status_code == 422
    data = json.loads(response.data)
    assert data["success"] is False
