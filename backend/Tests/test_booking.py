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


def setup_Data():
    student = client.post("/api/students", json={
        "name": "Ana",
        "email": "ana@test.com",
        "phone": "123",
        "course": "Beginner A1-A2",
        "status": "Active"
    }).json()

    teacher = client.post("/api/teachers", json={
        "name": "John",
        "email": "john@test.com",
        "course": "Beginner A1-A2"
    }).json()

    client.post(f"/api/teachers/{teacher['id']}/availability", json=[
        {"day": "Monday", "start": "10:00", "end": "11:00"}
    ])

    slots = client.get(f"/api/teachers/{teacher['id']}/available-slots").json()

    return student, teacher, slots


def test_booking_success():
    student, teacher, slots = setup_Data()

    res = client.post("/api/bookings", json={
        "studentId": student["id"],
        "teacherId": teacher["id"],
        "slots": [{"id": slots[0]["id"]}]
    })

    assert res.status_code == 200


def test_takenBooking_slot():
    student, teacher, slots = setup_Data()

    data = {
        "studentId": student["id"],
        "teacherId": teacher["id"],
        "slots": [{"id": slots[0]["id"]}]
    }

    client.post("/api/bookings", json=data)
    res = client.post("/api/bookings", json=data)

    assert res.status_code == 400


def test_invalidBooking_slot():
    student, teacher, _ = setup_Data()

    res = client.post("/api/bookings", json={
        "studentId": student["id"],
        "teacherId": teacher["id"],
        "slots": [{"id": 999}]
    })

    assert res.status_code == 400