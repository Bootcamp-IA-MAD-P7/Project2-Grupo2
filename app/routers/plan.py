from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..db.session import get_session
from ..core.security import get_current_user_sub
from ..services.plan import PlanService
from ..schemas.plan import PlanCreate, PlanResponse, PlanUpdate

router = APIRouter(prefix="/plans", tags=["plans"])
auth = Depends(get_current_user_sub)


@router.get("/", response_model=list[PlanResponse])
def list_plans(
    active: Optional[bool] = None,
    session: Session = Depends(get_session),
    _=auth
):
    return PlanService.get_all(session, active=active)


@router.post("/", response_model=PlanResponse, status_code=201)
def create_plan(
    data: PlanCreate,
    session: Session = Depends(get_session),
    _=auth
):
    return PlanService.create(session, data)


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(
    plan_id: int,
    session: Session = Depends(get_session),
    _=auth
):
    return PlanService.get_by_id(session, plan_id)


@router.patch("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    data: PlanUpdate,
    session: Session = Depends(get_session),
    _=auth
):
    return PlanService.update(session, plan_id, data)