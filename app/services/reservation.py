from datetime import date, datetime
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from fastapi import HTTPException

from app.models.reservation import Reservation, ReservationStatus
from app.models.shift import AvailableShift
from app.schemas.reservation import ReservationCreate


def create_reservation(session: Session, reservation_data: ReservationCreate, member_id: int) -> Reservation:
    shift = session.get(AvailableShift, reservation_data.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    active_count = session.exec(
        select(func.count(Reservation.id)).where(
            Reservation.shift_id == reservation_data.shift_id,
            Reservation.date == reservation_data.date,
            Reservation.status == ReservationStatus.confirmed
        )
    ).one()

    if active_count >= shift.max_capacity:
        raise HTTPException(status_code=409, detail="Shift is fully booked")

    existing = session.exec(
        select(Reservation).where(
            Reservation.member_id == member_id,
            Reservation.shift_id == reservation_data.shift_id,
            Reservation.date == reservation_data.date,
            Reservation.status == ReservationStatus.confirmed
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="You already have a reservation for this shift on this date")

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


def get_reservation(session: Session, reservation_id: int) -> Reservation:
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


def get_member_reservations(session: Session, member_id: int) -> List[Reservation]:
    return session.exec(
        select(Reservation).where(Reservation.member_id == member_id)
    ).all()


def get_shift_reservations(session: Session, shift_id: int, date: date) -> List[Reservation]:
    return session.exec(
        select(Reservation).where(
            Reservation.shift_id == shift_id,
            Reservation.date == date
        )
    ).all()


def cancel_reservation(session: Session, reservation_id: int) -> Reservation:
    reservation = get_reservation(session, reservation_id)
    if reservation.status == ReservationStatus.cancelled:
        raise HTTPException(status_code=400, detail="Reservation is already cancelled")
    reservation.status = ReservationStatus.cancelled
    reservation.updated_at = datetime.utcnow()
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def mark_no_show(session: Session, reservation_id: int) -> Reservation:
    reservation = get_reservation(session, reservation_id)
    if reservation.status != ReservationStatus.confirmed:
        raise HTTPException(status_code=400, detail="Only confirmed reservations can be marked as no-show")
    reservation.status = ReservationStatus.no_show
    reservation.updated_at = datetime.utcnow()
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation