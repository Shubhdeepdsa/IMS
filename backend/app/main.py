from fastapi import FastAPI

from app.api.api_router import api_router
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event('startup')
def startup_event() -> None:
    _ensure_initial_admin()


def _ensure_initial_admin() -> None:
    if not settings.first_superuser or not settings.first_superuser_password:
        return
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == settings.first_superuser).first()
        if not user:
            admin = User(
                username=settings.first_superuser,
                hashed_password=get_password_hash(settings.first_superuser_password),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


app.include_router(api_router)
