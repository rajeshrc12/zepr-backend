from app.core.database import DATABASE_URL  # get db url
from app.models.task import Base  # import your models
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# this is the Alembic Config object, which provides access to values in the .ini file.
config = context.config
fileConfig(config.config_file_name)

# Set the SQLAlchemy URL dynamically from .env
config.set_main_option('sqlalchemy.url', DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
