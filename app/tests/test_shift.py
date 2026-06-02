import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import date

SHIFT_DATA = {
    "class_name": "Yoga",
    "instructor": "Carlos",
    "day_of_week": "monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "max_capacity": 10,
    "active_slot": True
}


def test_create_shift(client: TestClient, auth_headers):
    r = client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["class_name"] == "Yoga"
    assert data["instructor"] == "Carlos"
    assert data["day_of_week"] == "monday"
    assert data["id"] is not None


def test_create_shift_invalid_capacity(client: TestClient, auth_headers):
    invalid = {**SHIFT_DATA, "max_capacity": 0}
    r = client.post("/api/v1/shifts/", json=invalid, headers=auth_headers)
    assert r.status_code == 422


def test_get_shift(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    r = client.get("/api/v1/shifts/1", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["class_name"] == "Yoga"


def test_get_shift_not_found(client: TestClient, auth_headers):
    r = client.get("/api/v1/shifts/999", headers=auth_headers)
    assert r.status_code == 404


def test_get_all_shifts(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    client.post("/api/v1/shifts/", json={
        **SHIFT_DATA,
        "day_of_week": "tuesday",
        "start_time": "11:00:00",
        "end_time": "12:00:00"
    }, headers=auth_headers)
    r = client.get("/api/v1/shifts/", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_all_shifts_filter_by_day(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    client.post("/api/v1/shifts/", json={
        **SHIFT_DATA,
        "day_of_week": "tuesday",
        "start_time": "11:00:00",
        "end_time": "12:00:00"
    }, headers=auth_headers)
    r = client.get("/api/v1/shifts/?day_of_week=monday", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["day_of_week"] == "monday"


def test_update_shift(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    r = client.patch("/api/v1/shifts/1", json={"instructor": "Maria"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["instructor"] == "Maria"
    assert r.json()["class_name"] == "Yoga"


def test_update_shift_not_found(client: TestClient, auth_headers):
    r = client.patch("/api/v1/shifts/999", json={"instructor": "Maria"}, headers=auth_headers)
    assert r.status_code == 404


def test_delete_shift(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    r = client.delete("/api/v1/shifts/1", headers=auth_headers)
    assert r.status_code == 200
    assert client.get("/api/v1/shifts/1", headers=auth_headers).status_code == 404


def test_delete_shift_not_found(client: TestClient, auth_headers):
    r = client.delete("/api/v1/shifts/999", headers=auth_headers)
    assert r.status_code == 404


def test_get_shift_availability(client: TestClient, auth_headers):
    client.post("/api/v1/shifts/", json=SHIFT_DATA, headers=auth_headers)
    r = client.get("/api/v1/shifts/1/availability?date=2026-06-02", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["max_capacity"] == 10
    assert data["active_bookings"] == 0
    assert data["available_spots"] == 10
    assert data["is_available"] is True


def test_get_shift_availability_not_found(client: TestClient, auth_headers):
    r = client.get("/api/v1/shifts/999/availability?date=2026-06-02", headers=auth_headers)
    assert r.status_code == 404