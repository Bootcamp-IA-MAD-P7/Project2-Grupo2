from datetime import date, datetime, timedelta, timezone

from sqlmodel import Session, select

from app.db.session import engine
from app.models.attendance import Attendance
from app.models.member import Member
from app.models.reservation import Reservation, ReservationStatus


def get_or_create_member(
    session: Session,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
) -> Member:
    existing_member = session.exec(
        select(Member).where(Member.email == email)
    ).first()

    if existing_member is not None:
        return existing_member

    member = Member(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        is_active=True,
    )

    session.add(member)
    session.commit()
    session.refresh(member)

    return member


def create_reservation(
    session: Session,
    member_id: int,
    reservation_date: date,
    status: ReservationStatus = ReservationStatus.confirmed,
) -> Reservation:
    reservation = Reservation(
        member_id=member_id,
        shift_id=None,
        date=reservation_date,
        status=status,
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


def create_attendance_if_not_exists(
    session: Session,
    member_id: int,
    reservation_id: int,
    check_in: datetime,
    check_out: datetime | None = None,
) -> Attendance | None:
    existing_attendance = session.exec(
        select(Attendance).where(
            Attendance.member_id == member_id,
            Attendance.reservation_id == reservation_id,
        )
    ).first()

    if existing_attendance is not None:
        return None

    attendance = Attendance(
        member_id=member_id,
        reservation_id=reservation_id,
        check_in=check_in,
        check_out=check_out,
    )

    session.add(attendance)
    session.commit()
    session.refresh(attendance)

    return attendance


def seed_attendance_data() -> None:
    with Session(engine) as session:
        today = date.today()

        member_1 = get_or_create_member(
            session=session,
            first_name="Laura",
            last_name="Gomez",
            email="laura.gomez@example.com",
            phone="600111111",
        )

        member_2 = get_or_create_member(
            session=session,
            first_name="Carlos",
            last_name="Perez",
            email="carlos.perez@example.com",
            phone="600222222",
        )

        member_3 = get_or_create_member(
            session=session,
            first_name="Marta",
            last_name="Lopez",
            email="marta.lopez@example.com",
            phone="600333333",
        )

        reservation_1 = create_reservation(
            session=session,
            member_id=member_1.id,
            reservation_date=today,
        )

        reservation_2 = create_reservation(
            session=session,
            member_id=member_2.id,
            reservation_date=today,
        )

        reservation_3 = create_reservation(
            session=session,
            member_id=member_3.id,
            reservation_date=today - timedelta(days=1),
        )

        reservation_4 = create_reservation(
            session=session,
            member_id=member_1.id,
            reservation_date=today - timedelta(days=2),
            status=ReservationStatus.cancelled,
        )

        create_attendance_if_not_exists(
            session=session,
            member_id=member_1.id,
            reservation_id=reservation_1.id,
            check_in=datetime.now(timezone.utc) - timedelta(hours=2),
            check_out=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        create_attendance_if_not_exists(
            session=session,
            member_id=member_2.id,
            reservation_id=reservation_2.id,
            check_in=datetime.now(timezone.utc) - timedelta(minutes=45),
            check_out=None,
        )

        create_attendance_if_not_exists(
            session=session,
            member_id=member_3.id,
            reservation_id=reservation_3.id,
            check_in=datetime.now(timezone.utc) - timedelta(days=1, hours=1),
            check_out=datetime.now(timezone.utc) - timedelta(days=1, minutes=20),
        )

        print("Attendance seed data created successfully.")
        print(f"Members: {member_1.id}, {member_2.id}, {member_3.id}")
        print(
            "Reservations created:",
            reservation_1.id,
            reservation_2.id,
            reservation_3.id,
            reservation_4.id,
        )


if __name__ == "__main__":
    seed_attendance_data()
    