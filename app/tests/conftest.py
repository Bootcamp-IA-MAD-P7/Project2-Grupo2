import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from decimal import Decimal
from datetime import date, timedelta

from main import app
from app.db.session import get_session
from app.models.membership import Membership, MembershipStatus
from app.models.payment import Payment, PaymentMethod, PaymentStatus


# ── Fixtures de infraestructura ────────────────────────────────────────────
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override():
        yield session
    app.dependency_overrides[get_session] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


# ── Auth (stub sin JWT real) ───────────────────────────────────────────────
@pytest.fixture(name="auth_headers")
def auth_headers_fixture():
    # Override get_current_user_sub para no necesitar un JWT real en tests
    from app.core.security import get_current_user_sub
    app.dependency_overrides[get_current_user_sub] = lambda: "test_user"
    return {}  # sin header real, la dependencia está mockeada


# ── Datos de prueba ────────────────────────────────────────────────────────
@pytest.fixture(name="monthly_plan")
def monthly_plan_fixture(session: Session):
    from app.models.plan import Plan
    plan = Plan(name="Monthly", price=Decimal("49.99"), duration_days=30, active=True)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@pytest.fixture(name="active_member")
def active_member_fixture(session: Session):
    from app.models.member import Member, MemberStatus
    m = Member(first_name="Carlos", last_name="García", email="carlos@gym.es",
               phone="+34600000001", status=MemberStatus.active)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m


@pytest.fixture(name="active_membership")
def active_membership_fixture(session: Session, active_member, monthly_plan):
    today = date.today()
    m = Membership(
        member_id=active_member.id, plan_id=monthly_plan.id,
        start_date=today, end_date=today + timedelta(days=30),
        status=MembershipStatus.active,
    )
    session.add(m)
    session.commit()
    session.refresh(m)
    return m
