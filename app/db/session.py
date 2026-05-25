from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


def create_db_and_tables():
    """Solo para tests — en producción usar Alembic."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependencia FastAPI. Uso:
        session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session
