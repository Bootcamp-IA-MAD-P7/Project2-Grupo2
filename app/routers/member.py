from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..db.session import get_session
from ..core.security import get_current_user_sub
from ..schemas.member import MemberCreate, MemberRead, MemberUpdate

router = APIRouter(prefix="/members", tags=["members"])
auth = Depends(get_current_user_sub)


@router.get("/", response_model=list[MemberRead])
def list_members(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
    _=auth
):
    from ..services.member import MemberService
    return MemberService.get_all(session, is_active=is_active, skip=skip, limit=limit)


@router.post("/", response_model=MemberRead, status_code=201)
def create_member(
    data: MemberCreate,
    session: Session = Depends(get_session),
    _=auth
):
    from ..services.member import MemberService
    return MemberService.create(session, data)


@router.get("/{member_id}", response_model=MemberRead)
def get_member(
    member_id: int,
    session: Session = Depends(get_session),
    _=auth
):
    from ..services.member import MemberService
    return MemberService.get_by_id(session, member_id)


@router.patch("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int,
    data: MemberUpdate,
    session: Session = Depends(get_session),
    _=auth
):
    from ..services.member import MemberService
    return MemberService.update(session, member_id, data)

@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, session: Session = Depends(get_session), _=auth):
    from ..services.member import MemberService
    MemberService.delete(session, member_id)
