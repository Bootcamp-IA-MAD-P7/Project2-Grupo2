from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.attendance import Attendance
from app.models.member import Member
from app.models.reservation import Reservation, ReservationStatus
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

    if not member.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance cannot be registered for an inactive member",
        )

    reservation = session.get(Reservation, attendance_data.reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    if reservation.member_id != attendance_data.member_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservation does not belong to this member",
        )

    if reservation.status != ReservationStatus.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance can only be registered for confirmed reservations",
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


def get_attendances(
    session: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Attendance]:
    statement = (
        select(Attendance)
        .order_by(Attendance.check_in.desc())
        .offset(offset)
        .limit(limit)
    )

    attendances = session.exec(statement).all()

    return attendances


def get_attendance_by_id(
    session: Session,
    attendance_id: int,
) -> Attendance:
    attendance = session.get(Attendance, attendance_id)

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found",
        )

    return attendance


def register_check_out(
    session: Session,
    attendance_id: int,
) -> Attendance:
    attendance = session.get(Attendance, attendance_id)

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found",
        )

    if attendance.check_out is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Check-out already registered for this attendance",
        )

    attendance.check_out = datetime.now(timezone.utc)

    session.add(attendance)
    session.commit()
    session.refresh(attendance)

    return attendance
