"""
Tests for deployment API endpoints
"""
import pytest
from flask import Flask
from implementation.api.rest.deployment_api import deployment_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(deployment_bp, url_prefix='/api')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_list_deployments(client):
    """Test listing deployments"""
    response = client.get('/api/deployments')
    assert response.status_code == 200
    data = response.get_json()
    assert 'deployments' in data
    assert 'total' in data


def test_create_deployment(client):
    """Test creating deployment"""
    payload = {
        'name': 'test-deployment',
        'environment': 'staging',
        'provider': 'aws',
        'region': 'us-east-1'
    }
    
    response = client.post('/api/deployments', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['deployment']['name'] == 'test-deployment'


def test_get_deployment(client):
    """Test getting deployment details"""
    response = client.get('/api/deployments/deploy-123')
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'status' in data


def test_update_deployment(client):
    """Test updating deployment"""
    payload = {'status': 'running'}
    response = client.put('/api/deployments/deploy-123', json=payload)
    assert response.status_code == 200


def test_delete_deployment(client):
    """Test deleting deployment"""
    response = client.delete('/api/deployments/deploy-123')
    assert response.status_code == 202


def test_scale_deployment(client):
    """Test scaling deployment"""
    payload = {'replicas': 5}
    response = client.post('/api/deployments/deploy-123/scale', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['replicas'] == 5
