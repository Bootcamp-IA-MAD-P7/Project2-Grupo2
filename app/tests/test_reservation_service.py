import pytest
from unittest.mock import MagicMock
from datetime import date, datetime
from app.models.reservation import Reservation, ReservationStatus
from app.models.shift import AvailableShift, DayOfWeek
from app.schemas.reservation import ReservationCreate
from app.services import reservation as reservation_service
from datetime import time


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def sample_shift():
    return AvailableShift(
        id=1,
        class_name="Yoga",
        instructor="Carlos",
        day_of_week=DayOfWeek.monday,
        start_time=time(9, 0),
        end_time=time(10, 0),
        max_capacity=10,
        active_slot=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_reservation():
    return Reservation(
        id=1,
        member_id=1,
        shift_id=1,
        date=date(2026, 6, 2),
        status=ReservationStatus.confirmed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def reservation_data():
    return ReservationCreate(
        shift_id=1,
        date=date(2026, 6, 2)
    )


def test_create_reservation_success(mock_session, sample_shift, reservation_data):
    mock_session.get.return_value = sample_shift
    mock_session.exec.return_value.one.return_value = 5  # 5 active bookings, capacity 10

    result = reservation_service.create_reservation(mock_session, reservation_data, member_id=1)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_create_reservation_shift_not_found(mock_session, reservation_data):
    mock_session.get.return_value = None
    result = reservation_service.create_reservation(mock_session, reservation_data, member_id=1)
    assert result is None


def test_create_reservation_class_full(mock_session, sample_shift, reservation_data):
    mock_session.get.return_value = sample_shift
    mock_session.exec.return_value.one.return_value = 10  # at capacity

    result = reservation_service.create_reservation(mock_session, reservation_data, member_id=1)
    assert result is None


def test_get_reservation_found(mock_session, sample_reservation):
    mock_session.get.return_value = sample_reservation
    result = reservation_service.get_reservation(mock_session, 1)
    assert result == sample_reservation
    mock_session.get.assert_called_once_with(Reservation, 1)


def test_get_reservation_not_found(mock_session):
    mock_session.get.return_value = None
    result = reservation_service.get_reservation(mock_session, 999)
    assert result is None


def test_get_member_reservations(mock_session, sample_reservation):
    mock_session.exec.return_value.all.return_value = [sample_reservation]
    result = reservation_service.get_member_reservations(mock_session, 1)
    assert len(result) == 1
    assert result[0].member_id == 1


def test_get_shift_reservations(mock_session, sample_reservation):
    mock_session.exec.return_value.all.return_value = [sample_reservation]
    result = reservation_service.get_shift_reservations(mock_session, 1, date(2026, 6, 2))
    assert len(result) == 1
    assert result[0].shift_id == 1


def test_cancel_reservation_found(mock_session, sample_reservation):
    mock_session.get.return_value = sample_reservation
    result = reservation_service.cancel_reservation(mock_session, 1)
    assert result.status == ReservationStatus.cancelled
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_cancel_reservation_not_found(mock_session):
    mock_session.get.return_value = None
    result = reservation_service.cancel_reservation(mock_session, 999)
    assert result is None


def test_mark_no_show_found(mock_session, sample_reservation):
    mock_session.get.return_value = sample_reservation
    result = reservation_service.mark_no_show(mock_session, 1)
    assert result.status == ReservationStatus.no_show
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_mark_no_show_not_found(mock_session):
    mock_session.get.return_value = None
    result = reservation_service.mark_no_show(mock_session, 999)
    assert result is None