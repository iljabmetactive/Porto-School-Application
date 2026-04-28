# how to run : pytest backend/Tests/test_student.py
# go to backend folder and run python -m pytest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sys
from unittest.mock import MagicMock

sys.modules["resend"] = MagicMock()

from fastapi.testclient import TestClient
from main import app
from database import Base, engine
import pytest

client = TestClient(app)

# Reset DB before each test to not hold state between tests
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_createStudent_success():
    res = client.post("/api/students", json={
        "name": "Ana",
        "email": "ana@test.com",
        "phone": "123",
        "course": "Beginner A1-A2",
        "status": "Active"
    })

    assert res.status_code == 200
    assert "id" in res.json()


def test_createStudent_missingNameValue():
    res = client.post("/api/students", json={
        "email": "ana@test.com",
        "phone": "123",
        "course": "Beginner A1-A2",
        "status": "Active"
    })

    assert res.status_code == 400


def test_createStudent_duplicateEmail():
    data = {
        "name": "Ana",
        "email": "ana@test.com",
        "phone": "123",
        "course": "Beginner A1-A2",
        "status": "Active"
    }

    client.post("/api/students", json=data)
    res = client.post("/api/students", json=data)

    assert res.status_code != 200

#student notes tests

def test_save_notes():
    student = client.post("/api/students", json={
        "name": "Ana",
        "email": "ana@test.com",
        "phone": "123",
        "course": "Beginner A1-A2",
        "status": "Active"
    }).json()

    res = client.post(f"/api/students/{student['id']}/notes", json={
        "notes": "test note"
    })

    assert res.status_code == 200