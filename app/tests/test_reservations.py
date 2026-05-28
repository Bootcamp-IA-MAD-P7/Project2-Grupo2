import pytest
from httpx import AsyncClient


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


async def create_shift(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)


@pytest.mark.anyio
async def test_create_reservation(client: AsyncClient):
    await create_shift(client)
    response = await client.post("/reservations/", json=RESERVATION_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["shift_id"] == 1
    assert data["status"] == "confirmed"
    assert data["id"] is not None


@pytest.mark.anyio
async def test_create_reservation_shift_not_found(client: AsyncClient):
    response = await client.post("/reservations/", json=RESERVATION_DATA)
    assert response.status_code == 409


@pytest.mark.anyio
async def test_create_reservation_class_full(client: AsyncClient):
    await client.post("/shifts/", json={**SHIFT_DATA, "max_capacity": 1})
    await client.post("/reservations/", json=RESERVATION_DATA)
    second = await client.post("/reservations/", json={**RESERVATION_DATA, "date": "2026-06-03"})
    assert second.status_code == 409


@pytest.mark.anyio
async def test_get_reservation(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.get("/reservations/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.anyio
async def test_get_reservation_not_found(client: AsyncClient):
    response = await client.get("/reservations/999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_member_reservations(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.get("/reservations/member/1")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_get_shift_reservations(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.get("/reservations/shift/1?date=2026-06-02")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_cancel_reservation(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.patch("/reservations/1/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


@pytest.mark.anyio
async def test_cancel_reservation_not_found(client: AsyncClient):
    response = await client.patch("/reservations/999/cancel")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_mark_no_show(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.patch("/reservations/1/no-show")
    assert response.status_code == 200
    assert response.json()["status"] == "no_show"


@pytest.mark.anyio
async def test_availability_decreases_after_reservation(client: AsyncClient):
    await create_shift(client)
    await client.post("/reservations/", json=RESERVATION_DATA)
    response = await client.get("/shifts/1/availability?date=2026-06-02")
    data = response.json()
    assert data["active_bookings"] == 1
    assert data["available_spots"] == 9