from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password
from sqlmodel import SQLModel
from app.core.security import (
    oauth2_scheme,
    blacklist_token,
)
from fastapi import Depends


router = APIRouter(prefix="/auth", tags=["auth"])


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(SQLModel):
    username: str
    password: str
    is_admin: bool = False


@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(subject=user.id))


@router.post("/register", response_model=dict)
def register(data: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(username=data.username, hashed_password=hash_password(data.password), is_admin=data.is_admin)
    session.add(user)
    session.commit()
    return {"message": "User created", "username": data.username}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    blacklist_token(token)

    return {
        "message": "Successfully logged out"
    }
