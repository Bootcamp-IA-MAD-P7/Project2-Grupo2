from datetime import date
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.shift import AvailableShift
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.shift import ShiftCreate, ShiftUpdate, ShiftAvailability
from app.models.shift import AvailableShift, DayOfWeek


def create_shift(session: Session, shift_data: ShiftCreate) -> AvailableShift:
    shift = AvailableShift.model_validate(shift_data)
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift


def get_shift(session: Session, shift_id: int) -> Optional[AvailableShift]:
    return session.get(AvailableShift, shift_id)


def get_all_shifts(
    session: Session,
    day_of_week: Optional[DayOfWeek] = None,
    name: Optional[str] = None
) -> List[AvailableShift]:
    statement = select(AvailableShift)
    if day_of_week:
        statement = statement.where(AvailableShift.day_of_week == day_of_week)
    if name:
        statement = statement.where(AvailableShift.name == name)
    return session.exec(statement).all()


def update_shift(session: Session, shift_id: int, shift_data: ShiftUpdate) -> Optional[AvailableShift]:
    shift = session.get(AvailableShift, shift_id)
    if not shift:
        return None
    update_data = shift_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shift, key, value)
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift


def delete_shift(session: Session, shift_id: int) -> bool:
    shift = session.get(AvailableShift, shift_id)
    if not shift:
        return False
    session.delete(shift)
    session.commit()
    return True


def get_shift_availability(session: Session, shift_id: int, date: date) -> Optional[ShiftAvailability]:
    shift = session.get(AvailableShift, shift_id)
    if not shift:
        return None

    statement = select(func.count(Reservation.id)).where(
        Reservation.shift_id == shift_id,
        Reservation.date == date,
        Reservation.status == ReservationStatus.confirmed
    )
    active_bookings = session.exec(statement).one()
    available_spots = shift.max_capacity - active_bookings

    return ShiftAvailability(
        shift_id=shift.id,
        shift_name=shift.class_name,
        date=date,
        day_of_week=shift.day_of_week,
        start_time=shift.start_time,
        end_time=shift.end_time,
        max_capacity=shift.max_capacity,
        active_bookings=active_bookings,
        available_spots=available_spots,
        is_available=available_spots > 0
    )