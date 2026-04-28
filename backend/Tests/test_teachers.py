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

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_teacher():
    res = client.post("/api/teachers", json={
        "name": "Teacher",
        "email": "t@test.com",
        "course": "Beginner A1-A2"
    })
    return res.json()["id"]

#create teacher tests

def test_createTeacher_success():
    res = client.post("/api/teachers", json={
        "name": "John",
        "email": "john@test.com",
        "course": "Beginner A1-A2"
    })

    assert res.status_code == 200
    assert "id" in res.json()


def test_createTeacher_missingEmailValue():
    res = client.post("/api/teachers", json={
        "name": "John",
        "course": "Beginner A1-A2"
    })

    assert res.status_code == 400


def test_createTeacher_missingNameValue():
    res = client.post("/api/teachers", json={
        "name": "",
        "email": "john@test.com",
        "course": "Beginner A1-A2"
    })

    assert res.status_code != 200


# booking tests

def test_setAvailability_success():
    teacher_id = create_teacher()

    res = client.post(f"/api/teachers/{teacher_id}/availability", json=[
        {"day": "Monday", "start": "10:00", "end": "11:00"}
    ])

    assert res.status_code == 200



def test_setAvailability_invalidTime():
    teacher_id = create_teacher()

    res = client.post(f"/api/teachers/{teacher_id}/availability", json=[
        {"day": "Monday", "start": "11:00", "end": "10:00"}
    ])

    assert res.status_code != 200


def test_setAvailability_empty():
    teacher_id = create_teacher()

    res = client.post(f"/api/teachers/{teacher_id}/availability", json=[])

    assert res.status_code != 200