from datetime import date, datetime, time, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.attendance import Attendance


def _validate_date_range(
    start_date: Optional[date],
    end_date: Optional[date],
) -> tuple[Optional[datetime], Optional[datetime]]:
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date",
        )

    start_datetime = None
    end_datetime = None

    if start_date is not None:
        start_datetime = datetime.combine(
            start_date,
            time.min,
            tzinfo=timezone.utc,
        )

    if end_date is not None:
        end_datetime = datetime.combine(
            end_date,
            time.max,
            tzinfo=timezone.utc,
        )

    return start_datetime, end_datetime


def get_attendances_for_csv(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    member_id: Optional[int] = None,
    reservation_id: Optional[int] = None,
) -> list[Attendance]:
    start_datetime, end_datetime = _validate_date_range(start_date, end_date)

    statement = select(Attendance)

    if start_datetime is not None:
        statement = statement.where(Attendance.check_in >= start_datetime)

    if end_datetime is not None:
        statement = statement.where(Attendance.check_in <= end_datetime)

    if member_id is not None:
        statement = statement.where(Attendance.member_id == member_id)

    if reservation_id is not None:
        statement = statement.where(Attendance.reservation_id == reservation_id)

    statement = statement.order_by(Attendance.check_in.desc())

    attendances = session.exec(statement).all()

    return attendances
