"""Tests for the Mergington High School Activities API."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity():
    response = client.post(
        "/activities/Chess Club/signup", params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 200
    assert "test@mergington.edu" in response.json()["message"]


def test_signup_duplicate_email_rejected():
    email = "dupe@mergington.edu"
    first = client.post(
        "/activities/Programming Class/signup", params={"email": email}
    )
    assert first.status_code == 200
    second = client.post(
        "/activities/Programming Class/signup", params={"email": email}
    )
    assert second.status_code == 400


def test_signup_unknown_activity():
    response = client.post(
        "/activities/Unknown Club/signup", params={"email": "x@mergington.edu"}
    )
    assert response.status_code == 404
