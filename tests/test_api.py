from fastapi.testclient import TestClient
import pytest
import sys
from pathlib import Path

# Ensure the `src` folder is importable during tests (no __init__.py in src)
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import app as app_module

client = TestClient(app_module.app)
activities = app_module.activities


def setup_function():
    # Reset in-memory activities to a known state before each test
    activities.clear()
    activities.update({
        "Test Club": {
            "description": "A test activity",
            "schedule": "Now",
            "max_participants": 5,
            "participants": ["existing@example.com"]
        }
    })


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Test Club" in data


def test_signup_new_participant():
    resp = client.post("/activities/Test%20Club/signup?email=new@example.com")
    assert resp.status_code == 200
    assert "Signed up new@example.com for Test Club" in resp.json().get("message", "")
    assert "new@example.com" in activities["Test Club"]["participants"]


def test_signup_duplicate_participant():
    resp = client.post("/activities/Test%20Club/signup?email=existing@example.com")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant():
    resp = client.delete("/activities/Test%20Club/participants?email=existing@example.com")
    assert resp.status_code == 200
    assert "Unregistered existing@example.com from Test Club" in resp.json().get("message", "")
    assert "existing@example.com" not in activities["Test Club"]["participants"]


def test_remove_nonexistent_participant():
    resp = client.delete("/activities/Test%20Club/participants?email=absent@example.com")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Participant not found for this activity"
