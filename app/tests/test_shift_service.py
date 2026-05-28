import pytest
from unittest.mock import MagicMock, patch
from datetime import time, date, datetime
from app.models.shift import AvailableShift, DayOfWeek
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.services import shift as shift_service


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


def test_create_shift(mock_session, sample_shift):
    shift_data = ShiftCreate(
        class_name="Yoga",
        instructor="Carlos",
        day_of_week=DayOfWeek.monday,
        start_time=time(9, 0),
        end_time=time(10, 0),
        max_capacity=10,
        active_slot=True
    )
    mock_session.refresh = MagicMock(side_effect=lambda x: setattr(x, "id", 1))

    result = shift_service.create_shift(mock_session, shift_data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_get_shift_found(mock_session, sample_shift):
    mock_session.get.return_value = sample_shift
    result = shift_service.get_shift(mock_session, 1)
    assert result == sample_shift
    mock_session.get.assert_called_once_with(AvailableShift, 1)


def test_get_shift_not_found(mock_session):
    mock_session.get.return_value = None
    result = shift_service.get_shift(mock_session, 999)
    assert result is None


def test_get_all_shifts_no_filter(mock_session, sample_shift):
    mock_session.exec.return_value.all.return_value = [sample_shift]
    result = shift_service.get_all_shifts(mock_session)
    assert len(result) == 1
    assert result[0].class_name == "Yoga"


def test_get_all_shifts_filter_by_day(mock_session, sample_shift):
    mock_session.exec.return_value.all.return_value = [sample_shift]
    result = shift_service.get_all_shifts(mock_session, day_of_week=DayOfWeek.monday)
    assert len(result) == 1
    assert result[0].day_of_week == DayOfWeek.monday


def test_update_shift_found(mock_session, sample_shift):
    mock_session.get.return_value = sample_shift
    shift_data = ShiftUpdate(instructor="Maria")
    result = shift_service.update_shift(mock_session, 1, shift_data)
    assert result.instructor == "Maria"
    assert result.class_name == "Yoga"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_update_shift_not_found(mock_session):
    mock_session.get.return_value = None
    shift_data = ShiftUpdate(instructor="Maria")
    result = shift_service.update_shift(mock_session, 999, shift_data)
    assert result is None


def test_delete_shift_found(mock_session, sample_shift):
    mock_session.get.return_value = sample_shift
    result = shift_service.delete_shift(mock_session, 1)
    assert result is True
    mock_session.delete.assert_called_once_with(sample_shift)
    mock_session.commit.assert_called_once()


def test_delete_shift_not_found(mock_session):
    mock_session.get.return_value = None
    result = shift_service.delete_shift(mock_session, 999)
    assert result is False


def test_get_shift_availability_found(mock_session, sample_shift):
    mock_session.get.return_value = sample_shift
    mock_session.exec.return_value.one.return_value = 3

    result = shift_service.get_shift_availability(mock_session, 1, date(2026, 6, 2))

    assert result.max_capacity == 10
    assert result.active_bookings == 3
    assert result.available_spots == 7
    assert result.is_available is True


def test_get_shift_availability_full(mock_session, sample_shift):
    mock_session.get.return_value = sample_shift
    mock_session.exec.return_value.one.return_value = 10

    result = shift_service.get_shift_availability(mock_session, 1, date(2026, 6, 2))

    assert result.available_spots == 0
    assert result.is_available is False


def test_get_shift_availability_not_found(mock_session):
    mock_session.get.return_value = None
    result = shift_service.get_shift_availability(mock_session, 999, date(2026, 6, 2))
    assert result is None