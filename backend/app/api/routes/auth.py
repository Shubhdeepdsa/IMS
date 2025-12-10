from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import authenticate_user, get_current_active_admin
from app.core.config import get_settings
from app.core.security import create_access_token, get_password_hash
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, Token

router = APIRouter()
settings = get_settings()


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(user.username, access_token_expires)
    return Token(access_token=access_token)


@router.post('/register', response_model=Token)
def register_user(payload: LoginRequest, db: Session = Depends(get_db), current_user=Depends(get_current_active_admin)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already taken')
    user = User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        role=UserRole.STAFF,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(user.username)
    return Token(access_token=access_token)
