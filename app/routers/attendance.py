import csv
import io
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.services.attendance_export_service import get_attendances_for_csv
from app.services.attendance_service import (
    create_attendance,
    get_attendance_by_id,
    get_attendances,
    register_check_out,
)


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
    description="Returns registered attendances with pagination.",
)
def list_attendances(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return get_attendances(session, offset, limit)


@router.get(
    "/export-csv",
    status_code=status.HTTP_200_OK,
    summary="Export attendances to CSV",
    description="Exports attendances to a CSV file with optional filters.",
)
def export_attendances_csv(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    member_id: Optional[int] = Query(default=None, ge=1),
    reservation_id: Optional[int] = Query(default=None, ge=1),
    session: Session = Depends(get_session),
):
    attendances = get_attendances_for_csv(
        session=session,
        start_date=start_date,
        end_date=end_date,
        member_id=member_id,
        reservation_id=reservation_id,
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "id",
            "member_id",
            "reservation_id",
            "check_in",
            "check_out",
        ]
    )

    for attendance in attendances:
        writer.writerow(
            [
                attendance.id,
                attendance.member_id,
                attendance.reservation_id,
                attendance.check_in.isoformat() if attendance.check_in else "",
                attendance.check_out.isoformat() if attendance.check_out else "",
            ]
        )

    output.seek(0)

    filename = f"attendances_{date.today().isoformat()}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get attendance by id",
    description="Returns the details of one attendance record.",
)
def get_attendance_detail(
    attendance_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return get_attendance_by_id(session, attendance_id)


@router.post(
    "/{attendance_id}/check-out",
    response_model=AttendanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Register attendance check-out",
    description="Registers the check-out time for an existing attendance.",
)
def register_attendance_check_out(
    attendance_id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
):
    return register_check_out(session, attendance_id)
