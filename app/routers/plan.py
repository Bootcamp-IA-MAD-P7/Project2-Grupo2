from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanResponse

router = APIRouter(prefix="/plans", tags=["plans"])

# RUTA PARA CREAR UN PLAN NUEVO
@router.post("/", response_model=PlanResponse)
def create_plan(plan: PlanCreate, db: Session = Depends(get_session)):
    db_plan = Plan.model_validate(plan)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# RUTA PARA OBTENER LA LISTA DE TODOS LOS PLANES
@router.get("/", response_model=List[PlanResponse])
def read_plans(db: Session = Depends(get_session)):
    plans = db.exec(select(Plan)).all()
    return plans