import pytest
from app.main import app
from app.models import url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear store before each test
        url_store._store.clear()
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_valid_url(client):
    """Test shortening a valid URL."""
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert len(data["short_code"]) == 6
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:5000/")

def test_shorten_invalid_url(client):
    """Test shortening an invalid URL."""
    response = client.post('/api/shorten', json={"url": "invalid"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_redirect_valid_short_code(client):
    """Test redirecting with a valid short code."""
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = response.get_json()["short_code"]
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == "https://example.com"

def test_redirect_invalid_short_code(client):
    """Test redirecting with an invalid short code."""
    response = client.get('/nonexist')
    assert response.status_code == 404

def test_stats_valid_short_code(client):
    """Test analytics for a valid short code."""
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = response.get_json()["short_code"]
    client.get(f'/{short_code}')  # Simulate a click
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["url"] == "https://example.com"
    assert data["clicks"] == 1
    assert "created_at" in data

def test_stats_invalid_short_code(client):
    """Test analytics for an invalid short code."""
    response = client.get('/api/stats/nonexist')
    assert response.status_code == 404