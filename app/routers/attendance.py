from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import create_attendance, get_attendances


router = APIRouter(
    prefix="/attendances",
    tags=["Attendances"],
)


@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register attendance",
    description="Registers the check-in of a member for an existing reservation.",
)
def register_attendance(
    attendance_data: AttendanceCreate,
    session: Session = Depends(get_session),
):
    return create_attendance(session, attendance_data)


@router.get(
    "/",
    response_model=list[AttendanceResponse],
    status_code=status.HTTP_200_OK,
    summary="List attendances",
    description="Returns all registered attendances.",
)
def list_attendances(
    session: Session = Depends(get_session),
):
    return get_attendances(session)
