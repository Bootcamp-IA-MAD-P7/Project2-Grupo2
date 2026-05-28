from datetime import date, datetime
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.reservation import Reservation, ReservationStatus
from app.models.shift import AvailableShift
from app.schemas.reservation import ReservationCreate


def create_reservation(session: Session, reservation_data: ReservationCreate, member_id: int) -> Optional[Reservation]:
    shift = session.get(AvailableShift, reservation_data.shift_id)
    if not shift:
        return None

    active_count = session.exec(
        select(func.count(Reservation.id)).where(
            Reservation.shift_id == reservation_data.shift_id,
            Reservation.date == reservation_data.date,
            Reservation.status == ReservationStatus.confirmed
        )
    ).one()

    if active_count >= shift.max_capacity:
        return None

    reservation = Reservation(
        member_id=member_id,
        shift_id=reservation_data.shift_id,
        date=reservation_data.date,
        status=ReservationStatus.confirmed
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def get_reservation(session: Session, reservation_id: int) -> Optional[Reservation]:
    return session.get(Reservation, reservation_id)


def get_member_reservations(session: Session, member_id: int) -> List[Reservation]:
    statement = select(Reservation).where(Reservation.member_id == member_id)
    return session.exec(statement).all()


def get_shift_reservations(session: Session, shift_id: int, date: date) -> List[Reservation]:
    statement = select(Reservation).where(
        Reservation.shift_id == shift_id,
        Reservation.date == date
    )
    return session.exec(statement).all()


def cancel_reservation(session: Session, reservation_id: int) -> Optional[Reservation]:
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return None
    reservation.status = ReservationStatus.cancelled
    reservation.updated_at = datetime.utcnow()
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def mark_no_show(session: Session, reservation_id: int) -> Optional[Reservation]:
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return None
    reservation.status = ReservationStatus.no_show
    reservation.updated_at = datetime.utcnow()
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation