from datetime import date
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..db.session import get_session
from ..core.security import get_current_user_sub
from ..schemas.reservation import ReservationCreate, ReservationRead
from ..services import reservation as reservation_service

router = APIRouter(prefix="/reservations", tags=["reservations"])
auth = Depends(get_current_user_sub)


@router.post("/", response_model=ReservationRead, status_code=201)
def create_reservation(
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session),
    current_user: int = Depends(get_current_user_sub)
):
    return reservation_service.create_reservation(session, reservation_data, member_id=current_user)


# Sub-routes BEFORE /{reservation_id} to avoid FastAPI routing conflict
@router.get("/member/{member_id}", response_model=List[ReservationRead])
def get_member_reservations(member_id: int, session: Session = Depends(get_session), _=auth):
    return reservation_service.get_member_reservations(session, member_id)


@router.get("/shift/{shift_id}", response_model=List[ReservationRead])
def get_shift_reservations(
    shift_id: int,
    date: date = Query(...),
    session: Session = Depends(get_session),
    _=auth
):
    return reservation_service.get_shift_reservations(session, shift_id, date)


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: int, session: Session = Depends(get_session), _=auth):
    return reservation_service.get_reservation(session, reservation_id)


@router.patch("/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_reservation(reservation_id: int, session: Session = Depends(get_session), _=auth):
    return reservation_service.cancel_reservation(session, reservation_id)


@router.patch("/{reservation_id}/no-show", response_model=ReservationRead)
def mark_no_show(reservation_id: int, session: Session = Depends(get_session), _=auth):
    return reservation_service.mark_no_show(session, reservation_id)