from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session #ver si se llama así o get_db_session o algo así, depende de cómo lo hayas nombrado en tu proyecto
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import create_attendance


router = APIRouter(
    prefix="/attendances",
    tags=["Attendances"],
)


@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_attendance(
    attendance_data: AttendanceCreate,
    session: Session = Depends(get_session),
):
    return create_attendance(attendance_data, session)