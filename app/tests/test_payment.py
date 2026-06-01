from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.payment import PaymentMethod, PaymentStatus


def test_create_payment(
    client: TestClient,
    session: Session,
    active_membership,
    active_member,
    monthly_plan,
):
    response = client.post(
        "/api/v1/payments/",
        json={
            "member_id": active_member.id,
            "membership_id": active_membership.id,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.card,
            "status": PaymentStatus.completed,
            "payment_date": str(date.today()),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["member_id"] == active_member.id
    assert data["membership_id"] == active_membership.id
    assert data["method"] == PaymentMethod.card
    assert data["status"] == PaymentStatus.completed


def test_create_payment_member_not_found(
    client: TestClient,
    active_membership,
    monthly_plan,
):
    response = client.post(
        "/api/v1/payments/",
        json={
            "member_id": 999,
            "membership_id": active_membership.id,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.cash,
            "status": PaymentStatus.completed,
            "payment_date": str(date.today()),
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


def test_create_payment_membership_not_found(
    client: TestClient,
    active_member,
    monthly_plan,
):
    response = client.post(
        "/api/v1/payments/",
        json={
            "member_id": active_member.id,
            "membership_id": 999,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.card,
            "status": PaymentStatus.completed,
            "payment_date": str(date.today()),
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Membership not found"


def test_get_payment(
    client: TestClient,
    session: Session,
    active_membership,
    active_member,
    monthly_plan,
):
    create_response = client.post(
        "/api/v1/payments/",
        json={
            "member_id": active_member.id,
            "membership_id": active_membership.id,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.transfer,
            "status": PaymentStatus.completed,
            "payment_date": str(date.today()),
        },
    )

    payment_id = create_response.json()["id"]

    response = client.get(f"/api/v1/payments/{payment_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == payment_id
    assert data["member_id"] == active_member.id


def test_get_payment_not_found(client: TestClient):
    response = client.get("/api/v1/payments/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_list_payments_with_pagination(
    client: TestClient,
    session: Session,
    active_member,
    active_membership,
    monthly_plan,
):
    for _ in range(3):
        client.post(
            "/api/v1/payments/",
            json={
                "member_id": active_member.id,
                "membership_id": active_membership.id,
                "amount": str(monthly_plan.price),
                "method": PaymentMethod.cash,
                "status": PaymentStatus.completed,
                "payment_date": str(date.today()),
            },
        )

    response = client.get("/api/v1/payments/?offset=0&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2


def test_list_payments_by_member(
    client: TestClient,
    active_member,
    active_membership,
    monthly_plan,
):
    client.post(
        "/api/v1/payments/",
        json={
            "member_id": active_member.id,
            "membership_id": active_membership.id,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.card,
            "status": PaymentStatus.completed,
            "payment_date": str(date.today()),
        },
    )

    response = client.get(f"/api/v1/payments/?member_id={active_member.id}")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(p["member_id"] == active_member.id for p in data)


def test_payment_pending_then_completed(
    client: TestClient,
    active_member,
    active_membership,
    monthly_plan,
):
    create_response = client.post(
        "/api/v1/payments/",
        json={
            "member_id": active_member.id,
            "membership_id": active_membership.id,
            "amount": str(monthly_plan.price),
            "method": PaymentMethod.card,
            "status": PaymentStatus.pending,
            "payment_date": str(date.today()),
        },
    )

    assert create_response.status_code == 201
    assert create_response.json()["status"] == PaymentStatus.pending

    payment_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/v1/payments/{payment_id}",
        json={"status": Pay