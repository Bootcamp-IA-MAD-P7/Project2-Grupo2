from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services import reservation as reservation_service

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/", response_model=ReservationRead, status_code=201)
def create_reservation(reservation_data: ReservationCreate, session: Session = Depends(get_session)):
    reservation = reservation_service.create_reservation(session, reservation_data, member_id=1)
    if not reservation:
        raise HTTPException(status_code=409, detail="Shift not found or class is full")
    return reservation


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = reservation_service.get_reservation(session, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.get("/member/{member_id}", response_model=List[ReservationRead])
def get_member_reservations(member_id: int, session: Session = Depends(get_session)):
    return reservation_service.get_member_reservations(session, member_id)


@router.get("/shift/{shift_id}", response_model=List[ReservationRead])
def get_shift_reservations(shift_id: int, date: date = Query(...), session: Session = Depends(get_session)):
    return reservation_service.get_shift_reservations(session, shift_id, date)


@router.patch("/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = reservation_service.cancel_reservation(session, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.patch("/{reservation_id}/no-show", response_model=ReservationRead)
def mark_no_show(reservation_id: int, session: Session = Depends(get_session)):
    reservation = reservation_service.mark_no_show(session, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation