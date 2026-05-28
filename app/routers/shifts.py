from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.models.shift import DayOfWeek
from app.schemas.shift import ShiftCreate, ShiftUpdate, ShiftRead, ShiftAvailability
from app.services import shift as shift_service

router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.post("/", response_model=ShiftRead, status_code=201)
def create_shift(shift_data: ShiftCreate, session: Session = Depends(get_session)):
    return shift_service.create_shift(session, shift_data)


@router.get("/", response_model=List[ShiftRead])
def get_all_shifts(
    day_of_week: Optional[DayOfWeek] = Query(default=None),
    name: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    return shift_service.get_all_shifts(session, day_of_week=day_of_week, name=name)


@router.get("/{shift_id}", response_model=ShiftRead)
def get_shift(shift_id: int, session: Session = Depends(get_session)):
    shift = shift_service.get_shift(session, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@router.patch("/{shift_id}", response_model=ShiftRead)
def update_shift(shift_id: int, shift_data: ShiftUpdate, session: Session = Depends(get_session)):
    shift = shift_service.update_shift(session, shift_id, shift_data)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@router.delete("/{shift_id}", status_code=200)
def delete_shift(shift_id: int, session: Session = Depends(get_session)):
    deleted = shift_service.delete_shift(session, shift_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shift not found")
    return {"message": "Shift deleted successfully"}


@router.get("/{shift_id}/availability", response_model=ShiftAvailability)
def get_shift_availability(shift_id: int, date: date = Query(...), session: Session = Depends(get_session)):
    availability = shift_service.get_shift_availability(session, shift_id, date)
    if not availability:
        raise HTTPException(status_code=404, detail="Shift not found")
    return availability