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


@pytest.mark.anyio
async def test_create_shift(client: AsyncClient):
    response = await client.post("/shifts/", json=SHIFT_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["class_name"] == "Yoga"
    assert data["instructor"] == "Carlos"
    assert data["day_of_week"] == "monday"
    assert data["id"] is not None


@pytest.mark.anyio
async def test_create_shift_invalid_capacity(client: AsyncClient):
    invalid = {**SHIFT_DATA, "max_capacity": 0}
    response = await client.post("/shifts/", json=invalid)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_shift(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    response = await client.get("/shifts/1")
    assert response.status_code == 200
    assert response.json()["class_name"] == "Yoga"


@pytest.mark.anyio
async def test_get_shift_not_found(client: AsyncClient):
    response = await client.get("/shifts/999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_all_shifts(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    await client.post("/shifts/", json={
        **SHIFT_DATA,
        "day_of_week": "tuesday",
        "start_time": "11:00:00",
        "end_time": "12:00:00"
    })
    response = await client.get("/shifts/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.anyio
async def test_get_all_shifts_filter_by_day(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    await client.post("/shifts/", json={
        **SHIFT_DATA,
        "day_of_week": "tuesday",
        "start_time": "11:00:00",
        "end_time": "12:00:00"
    })
    response = await client.get("/shifts/?day_of_week=monday")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["day_of_week"] == "monday"


@pytest.mark.anyio
async def test_update_shift(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    response = await client.patch("/shifts/1", json={"instructor": "Maria"})
    assert response.status_code == 200
    assert response.json()["instructor"] == "Maria"
    assert response.json()["class_name"] == "Yoga"


@pytest.mark.anyio
async def test_update_shift_not_found(client: AsyncClient):
    response = await client.patch("/shifts/999", json={"instructor": "Maria"})
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_shift(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    response = await client.delete("/shifts/1")
    assert response.status_code == 200
    assert (await client.get("/shifts/1")).status_code == 404


@pytest.mark.anyio
async def test_delete_shift_not_found(client: AsyncClient):
    response = await client.delete("/shifts/999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_shift_availability(client: AsyncClient):
    await client.post("/shifts/", json=SHIFT_DATA)
    response = await client.get("/shifts/1/availability?date=2026-06-02")
    assert response.status_code == 200
    data = response.json()
    assert data["max_capacity"] == 10
    assert data["active_bookings"] == 0
    assert data["available_spots"] == 10
    assert data["is_available"] is True


@pytest.mark.anyio
async def test_get_shift_availability_not_found(client: AsyncClient):
    response = await client.get("/shifts/999/availability?date=2026-06-02")
    assert response.status_code == 404