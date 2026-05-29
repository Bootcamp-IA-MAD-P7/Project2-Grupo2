from datetime import date, datetime, time, timezone
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.models.attendance import Attendance
from app.models.member import Member
from app.models.payment import Payment, PaymentStatus
from app.models.reservation import Reservation
from app.schemas.report import (
    AttendanceByMemberReport,
    AttendanceByReservationReport,
    AttendanceByShiftReport,
    AttendanceSummaryReport,
    IncomeReport,
)


def _validate_date_range(
    start_date: Optional[date],
    end_date: Optional[date],
) -> tuple[date, date]:
    today = date.today()

    if start_date is None:
        start_date = today

    if end_date is None:
        end_date = today

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date",
        )

    return start_date, end_date


def _date_range_to_datetimes(
    start_date: date,
    end_date: date,
) -> tuple[datetime, datetime]:
    start_datetime = datetime.combine(
        start_date,
        time.min,
        tzinfo=timezone.utc,
    )
    end_datetime = datetime.combine(
        end_date,
        time.max,
        tzinfo=timezone.utc,
    )

    return start_datetime, end_datetime


def get_attendance_summary_report(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> AttendanceSummaryReport:
    start_date, end_date = _validate_date_range(start_date, end_date)
    start_datetime, end_datetime = _date_range_to_datetimes(start_date, end_date)

    total_attendances = session.exec(
        select(func.count(Attendance.id)).where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
        )
    ).one()

    total_check_outs = session.exec(
        select(func.count(Attendance.id)).where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
            Attendance.check_out.is_not(None),
        )
    ).one()

    current_people_inside = session.exec(
        select(func.count(Attendance.id)).where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
            Attendance.check_out.is_(None),
        )
    ).one()

    return AttendanceSummaryReport(
        start_date=start_date,
        end_date=end_date,
        total_attendances=total_attendances,
        total_check_ins=total_attendances,
        total_check_outs=total_check_outs,
        current_people_inside=current_people_inside,
    )


def get_attendance_by_member_report(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[AttendanceByMemberReport]:
    start_date, end_date = _validate_date_range(start_date, end_date)
    start_datetime, end_datetime = _date_range_to_datetimes(start_date, end_date)

    statement = (
        select(
            Member.id,
            Member.first_name,
            Member.last_name,
            func.count(Attendance.id),
        )
        .join(Attendance, Attendance.member_id == Member.id)
        .where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
        )
        .group_by(Member.id, Member.first_name, Member.last_name)
        .order_by(func.count(Attendance.id).desc())
    )

    rows = session.exec(statement).all()

    return [
        AttendanceByMemberReport(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            total_attendances=total_attendances,
        )
        for member_id, first_name, last_name, total_attendances in rows
    ]


def get_attendance_by_reservation_report(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[AttendanceByReservationReport]:
    start_date, end_date = _validate_date_range(start_date, end_date)
    start_datetime, end_datetime = _date_range_to_datetimes(start_date, end_date)

    statement = (
        select(
            Reservation.id,
            Reservation.member_id,
            Reservation.date,
            func.count(Attendance.id),
        )
        .join(Attendance, Attendance.reservation_id == Reservation.id)
        .where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
        )
        .group_by(Reservation.id, Reservation.member_id, Reservation.date)
        .order_by(Reservation.date.desc(), func.count(Attendance.id).desc())
    )

    rows = session.exec(statement).all()

    return [
        AttendanceByReservationReport(
            reservation_id=reservation_id,
            member_id=member_id,
            reservation_date=reservation_date,
            total_attendances=total_attendances,
        )
        for reservation_id, member_id, reservation_date, total_attendances in rows
    ]


def get_attendance_by_shift_report(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[AttendanceByShiftReport]:
    start_date, end_date = _validate_date_range(start_date, end_date)
    start_datetime, end_datetime = _date_range_to_datetimes(start_date, end_date)

    statement = (
        select(
            Reservation.shift_id,
            Reservation.date,
            func.count(Attendance.id),
        )
        .join(Attendance, Attendance.reservation_id == Reservation.id)
        .where(
            Attendance.check_in >= start_datetime,
            Attendance.check_in <= end_datetime,
            Reservation.shift_id.is_not(None),
        )
        .group_by(Reservation.shift_id, Reservation.date)
        .order_by(Reservation.date.desc(), func.count(Attendance.id).desc())
    )

    rows = session.exec(statement).all()

    return [
        AttendanceByShiftReport(
            shift_id=shift_id,
            reservation_date=reservation_date,
            total_attendances=total_attendances,
        )
        for shift_id, reservation_date, total_attendances in rows
    ]


def get_income_report(
    session: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> IncomeReport:
    start_date, end_date = _validate_date_range(start_date, end_date)
    start_datetime, end_datetime = _date_range_to_datetimes(start_date, end_date)

    statement = select(
        func.coalesce(func.sum(Payment.amount), 0),
        func.count(Payment.id),
    ).where(
        Payment.payment_date >= start_datetime,
        Payment.payment_date <= end_datetime,
        Payment.status == PaymentStatus.completed,
    )

    total_income, total_payments = session.exec(statement).one()

    return IncomeReport(
        start_date=start_date,
        end_date=end_date,
        total_income=Decimal(total_income),
        total_payments=total_payments,
    )