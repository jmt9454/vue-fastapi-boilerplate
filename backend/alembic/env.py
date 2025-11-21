from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# --- 1. LOAD ENV VARS AND SYSTEM PATH ---
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# --- 2. IMPORT YOUR APP'S BASE AND MODELS ---
# This is critical! If you don't import them, Alembic thinks your DB is empty.
from app.core.database import Base
from app.models import * # Ensure app/models/__init__.py imports your classes!

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- 3. OVERRIDE ALEMBIC.INI WITH ENV VAR ---
# This ensures Alembic uses the REAL database url from .env,
# not the dummy one in alembic.ini
section = config.config_ini_section
config.set_section_option(section, "sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 4. SET TARGET METADATA ---
# This tells Alembic: "Look at this Base class to find tables"
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()