from app.db.session import engine
from app.models.base import Base  # type: ignore # ensures metadata import


def init_db() -> None:
    from app import models  # noqa: F401 ensures models imported
    Base.metadata.create_all(bind=engine)
