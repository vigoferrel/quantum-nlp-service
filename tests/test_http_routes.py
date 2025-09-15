#!/usr/bin/env python3
"""
Unit tests for Flask HTTP routes fixes
Tests the HTTP endpoints that were causing 404/405 errors
"""
import pytest
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask_app_fast import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_vigoleonrocks_get(client):
    """Test GET /api/vigoleonrocks returns 200"""
    response = client.get('/api/vigoleonrocks')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert data['service'] == 'quantum-nlp-service'
    print("✅ GET /api/vigoleonrocks returns 200")


def test_vigoleonrocks_post(client):
    """Test POST /api/vigoleonrocks returns 200"""
    response = client.post('/api/vigoleonrocks')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    print("✅ POST /api/vigoleonrocks returns 200")


def test_vigoleonrocks_options(client):
    """Test OPTIONS /api/vigoleonrocks returns 200"""
    response = client.options('/api/vigoleonrocks')
    assert response.status_code == 200
    print("✅ OPTIONS /api/vigoleonrocks returns 200")


def test_corporate_page(client):
    """Test GET /corporate returns 200"""
    response = client.get('/corporate')
    assert response.status_code in [200, 304]
    assert b'VIGOLEONROCKS' in response.data or response.status_code == 304
    print("✅ GET /corporate returns 200/304")


def test_favicon(client):
    """Test GET /favicon.ico returns 200"""
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert response.content_type == 'image/vnd.microsoft.icon'
    print("✅ GET /favicon.ico returns 200")


def test_metrics_endpoint(client):
    """Test GET /metrics returns 200"""
    response = client.get('/metrics')
    assert response.status_code == 200
    print("✅ GET /metrics returns 200")


def test_home_page(client):
    """Test GET / returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    print("✅ GET / returns 200")


def test_health_endpoint(client):
    """Test GET /health returns 200"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    print("✅ GET /health returns 200")


def test_api_status(client):
    """Test GET /api/status returns 200"""
    response = client.get('/api/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'operational'
    print("✅ GET /api/status returns 200")


def test_404_handler(client):
    """Test 404 error handler returns custom 404 page"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    # Should return HTML with our custom template or JSON error
    assert b'404' in response.data or 'Page not found' in response.get_json().get('error', '')
    print("✅ 404 handler works correctly")


if __name__ == "__main__":
    # Run tests directly for manual verification
    print("🧪 Running HTTP routes tests...")
    
    # Create test client manually
    app.config['TESTING'] = True
    client = app.test_client()
    
    test_vigoleonrocks_get(client)
    test_vigoleonrocks_post(client)
    test_vigoleonrocks_options(client)
    test_corporate_page(client)
    test_favicon(client)
    test_metrics_endpoint(client)
    test_home_page(client)
    test_health_endpoint(client)
    test_api_status(client)
    test_404_handler(client)
    
    print("🎉 All HTTP route tests passed!")
