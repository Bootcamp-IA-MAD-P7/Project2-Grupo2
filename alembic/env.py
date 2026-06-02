from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from sqlmodel import SQLModel
import os

from app.models.plan import Plan
from app.models.member import Member
from app.models.membership import Membership
from app.models.payment import Payment
from app.models.shift import AvailableShift
from app.models.reservation import Reservation
from app.models.attendance import Attendance
from app.models.user import User

config = context.config
<<<<<<< HEAD
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
=======
>>>>>>> developer

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

<<<<<<< HEAD

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
=======
DB_USER = os.getenv("DB_USER", "gymuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "gympassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "gym_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
>>>>>>> developer
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
<<<<<<< HEAD
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
=======
    connectable = create_engine(DATABASE_URL)
>>>>>>> developer
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
