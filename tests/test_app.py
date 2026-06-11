import pytest
import os
os.environ["API_KEY"] = "test-key"

from app import app as flask_app

KEY = "test-key"
AUTH = {"X-API-Key": KEY}


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_home_loads(client):
    r = client.get("/")
    assert r.status_code == 200

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"

def test_metrics_no_key(client):
    r = client.get("/api/metrics")
    assert r.status_code == 401

def test_metrics_wrong_key(client):
    r = client.get("/api/metrics", headers={"X-API-Key": "wrong"})
    assert r.status_code == 401

def test_metrics_valid_key(client):
    r = client.get("/api/metrics", headers=AUTH)
    assert r.status_code == 200
    data = r.get_json()
    assert "cpu"  in data
    assert "ram"  in data
    assert "temp" in data
    assert "fan"  in data
