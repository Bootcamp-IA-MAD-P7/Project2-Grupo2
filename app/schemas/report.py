from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttendanceSummaryReport(BaseModel):
    start_date: date
    end_date: date
    total_attendances: int
    total_check_ins: int
    total_check_outs: int
    current_people_inside: int

    model_config = ConfigDict(from_attributes=True)


class AttendanceByMemberReport(BaseModel):
    member_id: int
    first_name: str
    last_name: str
    total_attendances: int

    model_config = ConfigDict(from_attributes=True)


class AttendanceByReservationReport(BaseModel):
    reservation_id: int
    member_id: int
    reservation_date: date
    total_attendances: int

    model_config = ConfigDict(from_attributes=True)


class AttendanceByShiftReport(BaseModel):
    shift_id: int
    reservation_date: date
    total_attendances: int

    model_config = ConfigDict(from_attributes=True)


class IncomeReport(BaseModel):
    start_date: date
    end_date: date
    total_income: Decimal
    total_payments: int

    model_config = ConfigDict(from_attributes=True)


class ReportDateRange(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    