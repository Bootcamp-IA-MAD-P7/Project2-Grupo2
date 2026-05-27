from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["members"])

# RUTA PARA REGISTRAR UN MIEMBRO NUEVO
@router.post("/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_session)):
    db_member = Member.model_validate(member)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# RUTA PARA OBTENER LA LISTA DE TODOS LOS MIEMBROS
@router.get("/", response_model=List[MemberResponse])
def read_members(db: Session = Depends(get_session)):
    members = db.exec(select(Member)).all()
    return members