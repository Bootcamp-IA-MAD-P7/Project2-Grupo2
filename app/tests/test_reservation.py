import pytest
from fastapi.testclient import TestClient

SHIFT_DATA = {
    "class_name": "Yoga",
    "instructor": "Carlos",
    "day_of_week": "monday",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "max_capacity": 10,
    "active_slot": True
}

RESERVATION_DATA = {
    "shift_id": 1,
    "date": "2026-06-02"
}


def create_shift(client: TestClient, auth_headers, data=None):
    client.post("/shifts/", json=data or SHIFT_DATA, headers=auth_headers)


def test_create_reservation(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    r = client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["shift_id"] == 1
    assert data["status"] == "confirmed"
    assert data["id"] is not None


def test_create_reservation_shift_not_found(client: TestClient, auth_headers):
    r = client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    assert r.status_code == 404


def test_create_reservation_class_full(client: TestClient, auth_headers):
    create_shift(client, auth_headers, {**SHIFT_DATA, "max_capacity": 1})
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.post("/reservations/", json={**RESERVATION_DATA, "date": "2026-06-02"}, headers=auth_headers)
    assert r.status_code == 409


def test_get_reservation(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.get("/reservations/1", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_get_reservation_not_found(client: TestClient, auth_headers):
    r = client.get("/reservations/999", headers=auth_headers)
    assert r.status_code == 404


def test_get_member_reservations(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.get("/reservations/member/1", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_shift_reservations(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.get("/reservations/shift/1?date=2026-06-02", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_cancel_reservation(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.patch("/reservations/1/cancel", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"


def test_cancel_reservation_not_found(client: TestClient, auth_headers):
    r = client.patch("/reservations/999/cancel", headers=auth_headers)
    assert r.status_code == 404


def test_mark_no_show(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.patch("/reservations/1/no-show", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "no_show"


def test_availability_decreases_after_reservation(client: TestClient, auth_headers):
    create_shift(client, auth_headers)
    client.post("/reservations/", json=RESERVATION_DATA, headers=auth_headers)
    r = client.get("/shifts/1/availability?date=2026-06-02", headers=auth_headers)
    data = r.json()
    assert data["active_bookings"] == 1
    assert data["available_spots"] == 9