from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.core.security import get_current_user_sub
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import create_attendance, get_attendances

router = APIRouter(prefix="/attendances", tags=["Attendances"])
auth = Depends(get_current_user_sub)


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def register_attendance(
    attendance_data: AttendanceCreate,
    session: Session = Depends(get_session),
    _=auth
):
    return create_attendance(session, attendance_data)


@router.get("/", response_model=list[AttendanceResponse], status_code=status.HTTP_200_OK)
def list_attendances(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    _=auth
):
    return get_attendances(session, offset, limit)