from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.report import (
    AttendanceByMemberReport,
    AttendanceByReservationReport,
    AttendanceByShiftReport,
    AttendanceSummaryReport,
    IncomeReport,
)
from app.services.report_service import (
    get_attendance_by_member_report,
    get_attendance_by_reservation_report,
    get_attendance_by_shift_report,
    get_attendance_summary_report,
    get_income_report,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/attendance",
    response_model=AttendanceSummaryReport,
    status_code=status.HTTP_200_OK,
    summary="Get attendance summary report",
    description="Returns a summary of attendances within a date range.",
)
def get_attendance_summary(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_attendance_summary_report(session, start_date, end_date)


@router.get(
    "/attendance/by-member",
    response_model=list[AttendanceByMemberReport],
    status_code=status.HTTP_200_OK,
    summary="Get attendance report by member",
    description="Returns total attendances grouped by member within a date range.",
)
def get_attendance_by_member(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_attendance_by_member_report(session, start_date, end_date)


@router.get(
    "/attendance/by-reservation",
    response_model=list[AttendanceByReservationReport],
    status_code=status.HTTP_200_OK,
    summary="Get attendance report by reservation",
    description="Returns total attendances grouped by reservation within a date range.",
)
def get_attendance_by_reservation(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_attendance_by_reservation_report(session, start_date, end_date)


@router.get(
    "/attendance/by-shift",
    response_model=list[AttendanceByShiftReport],
    status_code=status.HTTP_200_OK,
    summary="Get attendance report by shift",
    description="Returns total attendances grouped by shift within a date range.",
)
def get_attendance_by_shift(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_attendance_by_shift_report(session, start_date, end_date)


@router.get(
    "/income",
    response_model=IncomeReport,
    status_code=status.HTTP_200_OK,
    summary="Get income report",
    description="Returns total completed payments within a date range.",
)
def get_income(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_income_report(session, start_date, end_date)
