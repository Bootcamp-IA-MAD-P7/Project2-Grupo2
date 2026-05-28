from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.attendance import Attendance
from app.models.member import Member
from app.models.reservation import Reservation
from app.schemas.attendance import AttendanceCreate


def create_attendance(
    session: Session,
    attendance_data: AttendanceCreate,
) -> Attendance:
    member = session.get(Member, attendance_data.member_id)

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    reservation = session.get(Reservation, attendance_data.reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    existing_attendance = session.exec(
        select(Attendance).where(
            Attendance.member_id == attendance_data.member_id,
            Attendance.reservation_id == attendance_data.reservation_id,
        )
    ).first()

    if existing_attendance is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance already registered for this member and reservation",
        )

    attendance = Attendance(
        member_id=attendance_data.member_id,
        reservation_id=attendance_data.reservation_id,
    )

    session.add(attendance)
    session.commit()
    session.refresh(attendance)

    return attendance